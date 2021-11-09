import database as db

"""Import Erzeugungsflächen"""
ortschaften = ['DIT', 'LAU', 'NFL', 'OHS', 'PIN', 'PLO', 'RDE', 'SEG', 'SLF', 'STE', 'STO']
sheetanuahl = [101, 88, 129, 83, 16, 24,169, 94, 123, 112 ,25]

print('Main Start')
dit = db.openLocationdata('Import\Standort', ortschaften[0], sheetanuahl[0]).openSheet()
dit53 = db.openLocationdata('Import\Standort', ortschaften[0], sheetanuahl[0]).opensingelSheetSpecial(53)
dit57 = db.openLocationdata('Import\Standort', ortschaften[0], sheetanuahl[0]).opensingelSheetSpecial(57)
dit59 = db.openLocationdata('Import\Standort', ortschaften[0], sheetanuahl[0]).opensingelSheetSpecial(59)
lau = db.openLocationdata('Import\Standort', ortschaften[1], sheetanuahl[1]).openSheet()
nfl = db.openLocationdata('Import\Standort', ortschaften[2], sheetanuahl[2]).openSheet()
ohs = db.openLocationdata('Import\Standort', ortschaften[3], sheetanuahl[3]).openSheet()
pin = db.openLocationdata('Import\Standort', ortschaften[4], sheetanuahl[4]).openSheet()
plo = db.openLocationdata('Import\Standort', ortschaften[5], sheetanuahl[5]).openSheet()
rde = db.openLocationdata('Import\Standort', ortschaften[6], sheetanuahl[6]).openSheet()
seg = db.openLocationdata('Import\Standort', ortschaften[7], sheetanuahl[7]).openSheet()
slf = db.openLocationdata('Import\Standort', ortschaften[8], sheetanuahl[8]).openSheet()
ste = db.openLocationdata('Import\Standort', ortschaften[9], sheetanuahl[9]).openSheetSTE()
sto = db.openLocationdata('Import\Standort', ortschaften[10], sheetanuahl[10]).openSheet()

"DataFrames zusammenführen und eine .csv Datei erstellen"

merge_df = dit.append(dit53, ignore_index=True)
print(merge_df)
merge_df = merge_df.append(dit57, ignore_index=True)
print(merge_df)
merge_df = merge_df.append(dit59, ignore_index=True)
print(merge_df)
merge_df = merge_df.append(lau, ignore_index=True)
print(merge_df)
merge_df = merge_df.append(nfl, ignore_index=True)
merge_df = merge_df.append(ohs, ignore_index=True)
merge_df = merge_df.append(pin, ignore_index=True)
merge_df = merge_df.append(plo, ignore_index=True)
merge_df = merge_df.append(rde, ignore_index=True)
merge_df = merge_df.append(seg, ignore_index=True)
merge_df = merge_df.append(slf, ignore_index=True)
merge_df = merge_df.append(ste, ignore_index=True)
merge_df = merge_df.append(sto, ignore_index=True)

exportname = "Datenbank/Wind/AusbauStandorte_gesamt_SH/"+ "AlleStandorte" + ".csv"
merge_df.to_csv(exportname, sep=';', encoding='utf-8', index=False)

