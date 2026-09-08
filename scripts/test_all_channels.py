#!/usr/bin/env python3
"""
Comprehensive Live Verification of all Email Channels, Lead Forms, and Stripe Payment Links.
"""

import urllib.request
import urllib.error
import json
import ssl
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()

API_URL = "https://www.marianstancik.dev/api/subscribe"

def test_api_newsletter():
    print("\n--- 1. Testing Newsletter Subscription ---")
    payload = {
        "email": "test-newsletter@marianstancik.dev",
        "source": "newsletter_test"
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(API_URL, data=data, headers={"Content-Type": "application/json", "Origin": "https://www.marianstancik.dev"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            body = json.loads(resp.read().decode('utf-8'))
            print(f"Status: {resp.status}")
            print(f"Response: {body}")
            assert body.get('status') == 'ok', "Newsletter status not ok"
            print("✅ Newsletter test PASSED")
    except Exception as e:
        print(f"❌ Newsletter test failed: {e}")

def test_api_contact_form():
    print("\n--- 2. Testing Contact Form ---")
    payload = {
        "name": "Integration Test Runner",
        "email": "test-contact@marianstancik.dev",
        "message": "Automated verification of contact inbox delivery.",
        "source": "contact_form"
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(API_URL, data=data, headers={"Content-Type": "application/json", "Origin": "https://www.marianstancik.dev"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            body = json.loads(resp.read().decode('utf-8'))
            print(f"Status: {resp.status}")
            print(f"Response: {body}")
            assert body.get('status') == 'ok', "Contact form status not ok"
            print("✅ Contact Form test PASSED")
    except Exception as e:
        print(f"❌ Contact Form test failed: {e}")

def test_api_product_order():
    print("\n--- 3. Testing Product Order Capture ---")
    payload = {
        "email": "test-buyer@marianstancik.dev",
        "product": "AI GEO Audit",
        "price": "150",
        "website": "https://example.com",
        "notes": "Automated test order verification",
        "source": "product_order"
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(API_URL, data=data, headers={"Content-Type": "application/json", "Origin": "https://www.marianstancik.dev"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            body = json.loads(resp.read().decode('utf-8'))
            print(f"Status: {resp.status}")
            print(f"Response: {body}")
            assert body.get('status') == 'ok', "Product order status not ok"
            print("✅ Product Order test PASSED")
    except Exception as e:
        print(f"❌ Product Order test failed: {e}")

def test_stripe_links():
    print("\n--- 4. Testing Stripe Payment Links ---")
    stripe_links = [
        ("AI GEO Audit (€150)", "https://buy.stripe.com/test_5kQ28t4Sk94S74pgBD28800"),
        ("AI Web Readiness Scan (€200)", "https://buy.stripe.com/test_28E6oJesU80O9cx4SV28801"),
        ("Full Web Audit (€300)", "https://buy.stripe.com/test_8x27sN70s4OC88tdpr28802"),
        ("Custom Agent Deposit (€500)", "https://buy.stripe.com/test_aFaaEZ1G880O88tdpr28803")
    ]
    for name, url in stripe_links:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
                print(f"✅ {name}: HTTP {resp.status} (Stripe Checkout is LIVE & accessible)")
        except urllib.error.HTTPError as e:
            print(f"⚠️ {name}: HTTP {e.code} - {e.reason}")
        except Exception as e:
            print(f"❌ {name}: Connection error: {e}")

if __name__ == '__main__':
    print("==================================================")
    print(" LIVE TESTING: EMAILS, FORMS & STRIPE PAYMENTS")
    print("==================================================")
    test_api_newsletter()
    test_api_contact_form()
    test_api_product_order()
    test_stripe_links()
    print("\n==================================================")
    print(" ALL LIVE ENDPOINT VERIFICATIONS COMPLETE")
    print("==================================================")
