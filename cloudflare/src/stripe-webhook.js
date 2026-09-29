/**
 * stripe-webhook.js — Stripe → D1 → audit trigger
 * 
 * Spracúva Stripe udalosti:
 *   checkout.session.completed → vytvorí client + spustí audit
 *   invoice.paid → predĺži subscription
 *   customer.subscription.deleted → zruší monitoring
 */

import { runAudit } from './audit-worker';

export async function handleStripeRequest(request, env) {
    // Only POST
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    // Verify Stripe signature (simple check)
    const signature = request.headers.get('stripe-signature');
    if (!signature) {
      return new Response('Missing signature', { status: 401 });
    }

    const body = await request.json();
    const event = body.type;
    const data = body.data?.object;

    if (!event || !data) {
      return new Response('Invalid payload', { status: 400 });
    }

    switch (event) {
      case 'checkout.session.completed': {
        // Nový one-time audit
        const domain = data.metadata?.domain || 
                       data.custom_fields?.find(f => f.key === 'domain')?.text?.value;
        const email = data.customer_details?.email;
        const name = data.customer_details?.name;
        const amount = data.amount_total;

        if (!domain || !email) {
          return new Response('Missing domain or email', { status: 400 });
        }

        // Create client
        const clientId = crypto.randomUUID();
        await env.DB.prepare(
          'INSERT INTO clients (id, email, domain, name, stripe_customer_id, plan) VALUES (?, ?, ?, ?, ?, ?)'
        ).bind(clientId, email, domain, name, data.customer, 'one-time').run();

        // Trigger audit
        await runAudit(domain, 'geo', env, clientId);

        return new Response(JSON.stringify({ client_id: clientId, status: 'audit_started' }), {
          headers: { 'content-type': 'application/json' }
        });
      }

      case 'invoice.paid': {
        // Subscription renewal
        const subId = data.subscription;
        const customerId = data.customer;

        const { results } = await env.DB.prepare(
          'SELECT id FROM clients WHERE stripe_customer_id = ?'
        ).bind(customerId).all();

        if (results.length) {
          await env.DB.prepare(
            'UPDATE subscriptions SET next_billing_at = ? WHERE stripe_subscription_id = ?'
          ).bind(
            new Date(data.lines?.data?.[0]?.period?.end * 1000).toISOString(),
            subId
          ).run();
        }
        break;
      }

      case 'customer.subscription.deleted': {
        const subId = data.id;
        await env.DB.prepare(
          'UPDATE subscriptions SET status = ? WHERE stripe_subscription_id = ?'
        ).bind('cancelled', subId).run();
        break;
      }
    }

    return new Response(JSON.stringify({ received: true }), {
      headers: { 'content-type': 'application/json' }
    });
  }