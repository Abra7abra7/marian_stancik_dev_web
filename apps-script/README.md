# Retencia leadov — Apps Script (právna vrstva v3.0.1)

Denná čistička podľa Zásad OOU v3.0.1 (07 Legal): kontakty so **status=pending** staršie
ako **30 dní** sa automaticky vymažú z hlavného hárku a archivujú do hárku
`archiv-odmietnute`. Confirmed kontakty sa nemažú — odchádzajú až odhlásením.

## Inštalácia (raz — Marián / IT, mimo repozitára)

1. Otvor Google Sheet s lead listom (zapisuje ho CRM relay webhook `api.marianstancik.dev/crm/`).
2. **Extensions → Apps Script** → vlož obsah `retention-cleanup.gs`.
3. Uprav konštanty v hlavičke skriptu: názov hárku s leadmi (`LEAD_SHEET_NAME`),
   číslo stĺpca so statusom (`STATUS_COLUMN`) a s dátumom odoslania (`DATE_COLUMN`).
4. **TODO:** v Google Workspace Admin konzole nastav **Data Region = Europe**
   (Sheets + Gmail) — deklarované v Zásadách OOU v3.0.1, nastavenie je mimo repozitára.
5. **Triggers → Add Trigger → `runRetentionCleanup` → Time-driven → Day timer**
   (napr. 03:00–04:00) → ulož a schváľ oprávnenia.

## Poznámky

- Skript predpokladá, že CRM relay webhook zapisuje do prvej záložky a riadky
  majú stĺpce `date` a `status` (status dopĺňa `/api/subscribe` = `pending`,
  `/api/confirm` = `confirmed`).
- Pri prvej inštalácii odporúčam najprv spustiť funkciu ručne a skontrolovať
  archívny hárok, až potom zapnúť denný trigger.
- Odhlásenie (unsubscribe) nie je súčasťou tohto skriptu — rieši odberateľský
  proces (1-klik odhlásenie podľa Zásad OOU).
