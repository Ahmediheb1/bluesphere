# BlueSphere's data

`experiments.csv` is built by `build_dataset.py` from the PSI test tables, copied as they are into the `PSI-*.csv` files (only extra spaces were removed). One row = one test, or a group of identical tests (column `n_tests`).

Units: oxygen in % by volume, pressure in kPa, air speed in cm/s, thickness in mm.

## How each table is read

**BASS-II (PSI-25), 129 tests.** The "Air display" column is read as the air speed in cm/s: the BASS-II tunnel imposed up to 40 cm/s. Values in parentheses and values after "pot" are fan potentiometer readings, not speeds, so they are ignored. "<1" becomes 0.5 cm/s. Oxygen is the calibrated initial value. The outcome comes from the words written in the table: "ext" or "extinguished" (went out as the air was reduced), "blowoff" (blown off by air that was too fast), "no ign" (no ignition), "off" (fan turned off, outcome unknown). With none of these words, the flame is counted as burning at the listed air speeds. The atlas point sits at the lowest recorded speed, or at the highest one for a blowoff. The raw text stays in the `notes` column.

**Saffire-I, II and III (PSI-98, 99, 100).** Read directly. For Saffire-II, oxygen was derived from the measured CO₂ (note 1 of the table). Sample 2-7 is split into two rows: the PMMA burned, the Nomex did not ignite. The Saffire-III table gives neither the oxygen nor the outcome, so its two tests are not on the map.

**FLEX (PSI-69), 274 droplets.** Grouped by fuel, pressure, oxygen, dilution (CO₂ or helium) and test end: 149 groups (`PSI-69_FLEX_grouped.csv`). "Extinction" = the flame went out before the droplet was gone; "Completion" and "Disruption" = the droplet burned. Still air (0 cm/s).

**ACME BRE (PSI-20), 194 flames.** The PSI table summarizes each day: the oxygen levels where flames ignited, and the number of flames ignited. One row per day and per oxygen level; the exact number per level is not known. "3400%" and "2100%" are read as 34% and 21%. Still air.

**FLEX-2 (PSI-68).** PSI only gives the ranges studied (17 to 30% O₂, 0.5 to 3 atm, 0.1 to 5 cm/s), not each test, so FLEX-2 is not on the map.

**CFI-G (PSI-159), 154 tests.** Inverse flames: oxygen (up to 85%) flows out of the burner into a fuel atmosphere. That is not the oxygen of the surrounding air, so CFI-G is not on the map. The tests are grouped in `PSI-159_CFI-G_grouped.csv`.
