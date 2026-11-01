/**
 * Retencia leadov podľa stavu opt-inu — právna vrstva v3.0.1 (07 Legal).
 *
 * Denný time-driven trigger:
 *  - nájde riadky so status = "pending" (e-mail odoslaný, opt-in nepotvrdený),
 *    ktorých dátum odoslania je starší ako PENDING_DAYS (30 dní),
 *  - skopíruje ich do archívneho hárku „archiv-odmietnute“ (v tom istom Spreadsheetu),
 *  - vymaže ich z hlavného hárku.
 *
 * Confirmed kontakty sa NEMAŽÚ — odchádzajú až odhlásením (unsubscribe), ktoré
 * spravuje odberateľský proces (mimo tohto skriptu).
 *
 * NASTAVENIE (raz, Marián / IT — mimo repozitára):
 *  1. Otvor Google Sheet s lead listom (ten, do ktorého zapisuje CRM relay
 *     webhook api.marianstancik.dev/crm/).
 *  2. Extensions > Apps Script → vlož tento súbor.
 *  3. Uprav konštanty nižšie (názov hárku, čísla stĺpcov) podľa reálnej štruktúry.
 *  4. TODO(Marián — Google Workspace Admin konzola): Data Region = Europe
 *     (Sheets + Gmail) — nastavenie mimo repozitára, deklarované v Zásadách OOU v3.0.1.
 *  5. Triggers > Add Trigger > runRetentionCleanup > Time-driven > Day timer >
 *     vyber čas (napr. 03:00–04:00) > Save (súhlas s oprávneniami).
 */

// ---------- KONFIGURÁCIA (upraviť podľa reálneho Sheets) ----------
const LEAD_SHEET_NAME = 'newsletter';      // názov hárku s leadmi (prvá záložka relay webhooku)
const ARCHIVE_SHEET_NAME = 'archiv-odmietnute';
const PENDING_DAYS = 30;                   // Zásady OOU v3.0.1: pending 30 dní
const STATUS_COLUMN = 10;                  // stĺpec so statusom (pending/confirmed) — upraviť
const DATE_COLUMN = 8;                     // stĺpec s dátumom odoslania (YYYY-MM-DD) — upraviť
// ---------------------------------------------------------------

function runRetentionCleanup() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(LEAD_SHEET_NAME);
  if (!sheet) {
    console.error('Sheet not found: ' + LEAD_SHEET_NAME);
    return;
  }

  let archive = ss.getSheetByName(ARCHIVE_SHEET_NAME);
  if (!archive) {
    archive = ss.insertSheet(ARCHIVE_SHEET_NAME);
    // hlavičku archívu skopíruj z hlavného hárku
    const headerCount = sheet.getLastColumn();
    archive.getRange(1, 1, 1, headerCount).setValues(sheet.getRange(1, 1, 1, headerCount).getValues());
    archive.getRange(1, headerCount + 1).setValue('archived_at');
  }

  const lastRow = sheet.getLastRow();
  if (lastRow < 2) return; // žiadne dáta

  const headerCount = sheet.getLastColumn();
  const data = sheet.getRange(2, 1, lastRow - 1, headerCount).getValues();
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - PENDING_DAYS);
  const cutoffIso = Utilities.formatDate(cutoff, Session.getScriptTimeZone(), 'yyyy-MM-dd');

  const toArchive = [];
  const keep = [];
  for (const row of data) {
    const status = String(row[STATUS_COLUMN - 1] || '').trim().toLowerCase();
    const sentDate = row[DATE_COLUMN - 1];
    const sentIso = (sentDate instanceof Date)
      ? Utilities.formatDate(sentDate, Session.getScriptTimeZone(), 'yyyy-MM-dd')
      : String(sentDate || '').slice(0, 10);

    if (status === 'pending' && sentIso && sentIso < cutoffIso) {
      const archived = row.slice();
      archived[headerCount - 1] = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd HH:mm:ss');
      toArchive.push(archived);
    } else {
      keep.push(row);
    }
  }

  if (toArchive.length === 0) return;

  // 1. archivácia
  archive.getRange(archive.getLastRow() + 1, 1, toArchive.length, toArchive[0].length).setValues(toArchive);

  // 2. prepis hlavného hárku bez vymazaných riadkov
  sheet.getRange(2, 1, data.length, headerCount).clearContent();
  if (keep.length > 0) {
    sheet.getRange(2, 1, keep.length, headerCount).setValues(keep);
  }

  console.log('Retention cleanup: ' + toArchive.length + ' pending kontaktov archivovaných a vymazaných (>' + PENDING_DAYS + ' dní).');
}
