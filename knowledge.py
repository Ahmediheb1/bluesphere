"""La base de connaissances de l'assistant : seulement des faits tirés de sources de la NASA.

Chaque fait porte l'étiquette de sa source, par exemple [S4]. L'application affiche ensuite
la liste des sources citées, avec leurs liens. Pour ajouter un fait, ajouter sa source dans
SOURCES et l'étiqueter dans FACTS.
"""

SOURCES = {
    "S1": ("NASA Space Apps 2026, challenge « Flame in Freefall »",
           "https://www.spaceappschallenge.org/2026/challenges/flame-in-freefall/"),
    "S2": ("NASA, A Researcher's Guide to: Combustion Science (2015)",
           "https://www.nasa.gov/missions/station/a-researchers-guide-to-combustion-science/"),
    "S3": ("NASA Glenn, Combustion Science (FM2, SoFIE, FLARE)",
           "https://www.nasa.gov/glenn/glenn-expertise-space-exploration/physical-sciences-program/combustion-science/"),
    "S4": ("Ferkul et al., 2017, Results of Large-Scale Spacecraft Flammability Tests (NASA)",
           "https://ntrs.nasa.gov/api/citations/20170008805/downloads/20170008805.pdf"),
    "S5": ("Fortenberry et al., 2021, Combustion Products from Saffire-IV and Saffire-V (ICES)",
           "https://ttu-ir.tdl.org/items/13a0b598-7e79-4d08-9d42-1fd220ad8803"),
    "S6": ("Brooker and Niehaus, 2022, Model Development of Large-Scale Spacecraft Fires during Saffire-IV (NASA)",
           "https://ntrs.nasa.gov/citations/20220002714"),
    "S7": ("Brooker et al., 2015, Modeling and Analysis of Realistic Fire Scenarios in Spacecraft (NASA)",
           "https://ntrs.nasa.gov/api/citations/20150021283/downloads/20150021283.pdf"),
    "S8": ("Olson et al., 2009, Flame spread over thin fuels in actual and simulated microgravity, Combustion and Flame",
           "https://doi.org/10.1016/j.combustflame.2009.01.015"),
    "S9": ("Ross et al., combustion experiments on Mir (NASA SP-4225)", None),
    "S10": ("Greenberg et al., 1999, Microgravity combustion diagnostics, Meas. Sci. Technol. (NASA Glenn)",
            "https://iopscience.iop.org/0957-0233/10/10/301"),
    "S11": ("NASA PSI, BASS-II (PSI-25), DOI 10.60555/4qc4-de67",
            "https://psi.nasa.gov/physci/repo/data/investigations/PSI-25"),
    "S12": ("NASA PSI, Saffire-I, II and III (PSI-98, 99, 100)",
            "https://psi.nasa.gov/physci/repo/data/investigations/PSI-98"),
    "S13": ("NASA PSI, FLEX (PSI-69) and FLEX-2 (PSI-68)",
            "https://psi.nasa.gov/physci/repo/data/investigations/PSI-69"),
    "S14": ("NASA PSI, ACME BRE (PSI-20) and CFI-G (PSI-159)",
            "https://psi.nasa.gov/physci/repo/data/investigations/PSI-20"),
    "S15": ("Abercromby et al., 2022, NASA DCS Strategic Plan: exploration atmosphere 8.2 psia / 34% O2 (NASA)",
            "https://ntrs.nasa.gov/api/citations/20220005709/downloads/AsMA%202022%20-%20Abercromby%20-%20DCS%20Strategic%20Plan%20v2.pdf"),
    "S16": ("Norcross et al., 2013, Effects of the 8 psia / 32% O2 Atmosphere on the Human in the Spaceflight Environment (NASA TM)",
            "https://ntrs.nasa.gov/citations/20130013505"),
    "S17": ("NASA history: Apollo 1, and the 1997 fire aboard Mir",
            "https://www.nasa.gov/history/25-years-ago-fire-aboard-space-station-mir/"),
    "S18": ("BlueSphere, analysis of the PSI test tables (method in DATA.md)",
            "https://github.com/Ahmediheb1/bluesphere/blob/main/DATA.md"),
}

FACTS = """
## Fire in space: the challenge and the history
- The future Moon base and pressurized rovers will probably have 30% oxygen or more, at 10.2 psi or less. That is more than 40% more oxygen than Earth's air (21%), which makes materials much more flammable. The reason is to shorten the preparation before moonwalks. [S1]
- Spacesuits are filled with pure oxygen at 4.3 psi, against 14.7 psi at sea level. Astronauts breathe pure oxygen before going out, to avoid decompression sickness. [S1]
- Real incidents: Apollo 1 (1967, three astronauts died in a cabin filled with oxygen during a ground test), the oxygen tank explosion on Apollo 13, the fire aboard Mir caused by an oxygen generator (1997), and a smoke alarm during Artemis II. [S1] [S17]
- NASA's fire safety rests on three pillars: prevention (choice of materials), detection (smoke) and extinguishment. [S1]
- PSI holds no combustion data in partial gravity for now. Future experiments are planned (LUCI and FM2). ACME E-FIELD imitated partial gravity with an electric field. [S1]
- Spinoffs on Earth: fine water-mist extinguishers developed for the station, smoke detection, firefighters' clothing and air tanks. [S1]

## How flames behave in microgravity
- Without gravity, hot air does not rise, so a flame does not go up: it becomes a sphere that depends on oxygen diffusion. [S1] [S2]
- Flames spread best around 10 cm/s, the typical speed of spacecraft ventilation. [S2]
- NASA lists "a fire will self-extinguish if the ventilation is shut off" as a misconception. Invisible cool flames can reignite long after. [S2]
- When the air slows down, a flame can break into flamelets about 1 cm wide that keep burning below the extinction limit. If the air goes from 0.5 to 50 cm/s, a flamelet can grow by 200% in less than 10 seconds. [S8]
- On Mir, a candle burned for up to 45 minutes with a flame too faint for the cameras. After extinction, a flammable cloud remained. Shutting off the ventilation often puts the fire out, but not always. [S9]

## Large fires in Cygnus (Saffire)
- Saffire-I: a 94 cm SIBAL fabric sample (cotton and fiberglass) at 20 cm/s burned with a flame spread rate of 1.8 mm/s for 420 s, releasing about 1,200 W. The oxygen in the module only dropped from 21.7% to 21.5%, so oxygen is a weak fire signal. [S4]
- Saffire-I: the same fabric burned 420 seconds with the air flowing in the direction of the flame, against 70 seconds with the air flowing against it. [S4] [S12]
- Saffire-II: thin silicone burns on Earth but did not burn in microgravity. Nomex, rated safe by the NASA-STD-6001 standard, did not ignite. [S4]
- Saffire-IV and V: far from the fire, CO2 starts rising about 50 s after ignition; CO rises more slowly. The cabin, about 18 m3, is mixed in about 6 minutes. The smoke-eater filter did not remove CO in a noticeable way. [S5]
- Saffire-V burned at 26.5% O2 under reduced pressure (about 10.4 psi): it is the real fire closest to the future Moon base air. [S5]
- Saffire-IV model: at the far sensor, CO2 reached 1.4 times its starting value with SIBAL and 2.8 times with PMMA. Sensors placed in the outflow react first. [S6]
- Saffire-IV: the PMMA flame went out when the ventilation was lowered, but the hot fuel kept releasing vapors. When the fan came back, a deflagration reignited it. [S6]
- NASA combines a detailed but slow fire model (FDS) with a fast single-zone model, to compare cabin volumes and fire sizes. In these models, the fire is imposed, not predicted. [S7]

## NASA test data in PSI (the investigations used by BlueSphere)
- BASS-II (Burning and Suppression of Solids II): burning and extinction of solids (SIBAL fabric, PMMA, Nomex, candle) in a small wind tunnel up to 40 cm/s in the Microgravity Science Glovebox, with oxygen lowered below 21% by adding nitrogen. 129 tests. [S11]
- Saffire-I, II and III: large fires set on purpose inside uncrewed Cygnus spacecraft after they left the ISS. Saffire-II burned nine 29 x 5 cm samples, with an Earth comparison. [S12]
- FLEX: 274 methanol and heptane droplets in still air, with suppression by dilution with CO2 or helium, from 0.7 to 3 atm. Some droplets burned at 30 to 34% O2 at 0.7 atm, an atmosphere close to the Moon base. FLEX-2: droplets of eight fuels from 17 to 30% O2 and 0.5 to 3 atm (PSI only gives the ranges). [S13]
- ACME BRE: 194 gas flames that emulate the burning of materials, in still air, from 21 to 40% O2. CFI-G: 154 inverse flames where a mixture of up to 85% O2 flows from a spherical burner into a fuel atmosphere. [S14]
- Instruments of the Combustion Integrated Rack: visible, UV and infrared cameras, a gas chromatograph, pressure sensors and accelerometers, plus soot, temperature and velocity measurements. [S10]

## Atmospheres for exploration
- NASA recommends 8.2 psia (56.5 kPa), 34% O2 and 66% N2 for vehicles supporting frequent spacewalks (the exploration atmosphere), as a compromise between flammability, hypoxia and decompression sickness. [S15]
- This 8.2 psia / 34% atmosphere is physiologically equivalent to the 10.2 psia / 26.5% O2 staged atmosphere used on 34 Space Shuttle missions. [S16]

## What the NASA data does not cover yet (BlueSphere analysis of PSI)
- BlueSphere gathers 764 real NASA tests from 8 PSI investigations. [S18]
- No solid material was tested above 22.2% O2 in these PSI tables. The 39 conditions tested at 30% O2 or more are all gases (ACME BRE) or liquid droplets (FLEX). [S18]
- The lowest oxygen level where a solid burned in these tables is 14.2% (BASS-II). [S18]
- None of these tests was run in lunar or Martian gravity: the Moon base (30% O2 or more, lunar gravity) is a no-data zone. [S18] [S1]
- Ongoing NASA experiments aim at these gaps: FM2, the first combustion experiment on the Moon; SoFIE, up to 85% O2 with the same oxygen partial pressure as on Earth; FLARE, linking flammability limits measured on the ground and in microgravity. [S3]
"""

ABOUT_BLUESPHERE = """
## About BlueSphere itself (the team's method, not NASA data)
- BlueSphere's risk score uses the team's expert weighting, version 1: oxygen 30%, material 25%, ventilation 25%, thickness 10%, pressure 10%. Gravity changes the confidence, not the score. In a no-data zone, cautious mode adds a 10-point safety margin.
- BlueSphere's detection rules: CO2 gives the alert, CO confirms it; the speed of change matters more than the value; combine temperature, O2, CO2 and CO rather than one signal.
- BlueSphere is a decision-support tool. It does not certify a habitat.
"""
