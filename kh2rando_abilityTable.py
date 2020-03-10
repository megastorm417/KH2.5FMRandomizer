from khenum import AbilityClass,KHCharacter,AbilityTable_enum,AbilityType,AbilityTypeGained
currentChar1 = KHCharacter.Sora
currentChar2 = KHCharacter.Donald
currentChar3 = KHCharacter.Goofy
Ability_Table = {
AbilityTable_enum.Action : {

     'Guard'                     :(currentChar1,              0x052),
     'Upper Slash'                     :(currentChar1,              0x089),
     'Horizontal Slash'                     :(currentChar1,              0x10F),
     'Finishing Leap'                     :(currentChar1,              0x10B),
     'Retaliating Slash'                     :(currentChar1,              0x111),
     'Slapshot'                     :(currentChar1,              0x106),
     'Dodge Slash'                     :(currentChar1,              0x107),
     'Flash Step'                     :(currentChar1,              0x22F),
     'Slide Dash'                     :(currentChar1,              0x108),
     'Vicinity Break'                     :(currentChar1,              0x232),
     'Guard Break'                     :(currentChar1,              0x109),
     'Explosion'                     :(currentChar1,              0x10A),
     'Aerial Sweep'                     :(currentChar1,              0x10D),
     'Aerial Dive'                     :(currentChar1,              0x230),
     'Aerial Spiral'                     :(currentChar1,              0x10E),
     'Aerial Finish'                     :(currentChar1,              0x110),
     'Magnet Burst'                     :(currentChar1,              0x231),
     'Counterguard'                     :(currentChar1,              0x10C),
     'Auto Summon'                     :(currentChar1,              0x185),
     'Auto Wisdom'                     :(currentChar1,              0x182),
     'Auto-Limit'                     :(currentChar1,              0x238),
     'Trinity Limit'                     :(currentChar1,              0x0C6),



    'Donald Fire'               :(currentChar2,             0x0A5),
    'Donald Blizzard'           :(currentChar2,             0x0A6),
    'Fantasia'                  :(currentChar2,              0x0C7),
    'Flare Force'               :(currentChar2,              0x0C8),



    'Goofy Tornado'               :(currentChar3,             0x1A7),
    'Goofy Turbo'           :(currentChar3,             0x1A9),
    'Tornado Fusion'                  :(currentChar3,              0x0C9),
    'Teamwork'               :(currentChar3,              0x0CA),

},
AbilityTable_enum.Support : {

    'Scan'               :(currentChar1,             0x08A, 1),
    'Aerial Recovery'               :(currentChar1,             0x09E, 1),
    'Combo Master'               :(currentChar1,             0x21B, 1),
    'Summon Boost'               :(currentChar1,             0x18F, 1,AbilityType.Additive),


    'MP Haste (DriveAbility)'                                  :(currentChar1,             0x19D, 1,AbilityType.Additive,AbilityTypeGained.DriveForm),
    'Combo Plus (DriveAbility)'                                :(currentChar1,             0x0A2, 2,AbilityType.Additive,AbilityTypeGained.DriveForm),
    'Air Combo Plus (DriveAbility)'                            :(currentChar1,             0x0A3, 2,AbilityType.Additive,AbilityTypeGained.DriveForm),
    'Form Boost (DriveAbility)'                                :(currentChar1,             0x18E, 2,AbilityType.Additive,AbilityTypeGained.DriveForm),
    'Draw (DriveAbility)'                                      :(currentChar1,             0x195, 1,AbilityType.Additive,AbilityTypeGained.DriveForm),
    'Lucky Lucky (DriveAbility)'                               :(currentChar1,             0x197, 1,AbilityType.Additive,AbilityTypeGained.DriveForm),
    'MP Rage (DriveAbility)'                                   :(currentChar1,             0x19C, 1,AbilityType.Additive,AbilityTypeGained.DriveForm),
    'Lucky Lucky (CritcalBonus)'                :(currentChar1,             0x197, 2,AbilityType.Additive,AbilityTypeGained.CriticalBonus),
    'Reaction Boost (CritcalBonus)'             :(currentChar1,             0x188, 1,AbilityType.Additive,AbilityTypeGained.CriticalBonus),
    'Finishing Plus (CritcalBonus)'             :(currentChar1,             0x189, 1,AbilityType.Additive,AbilityTypeGained.CriticalBonus),
    'MP Hastera (CritcalBonus)'                 :(currentChar1,             0x1A5, 1,AbilityType.Additive,AbilityTypeGained.CriticalBonus),
    'Draw (CritcalBonus)'                       :(currentChar1,             0x195, 1,AbilityType.Additive,AbilityTypeGained.CriticalBonus),
    #'NoEXP (CritcalBonus)'                       :(currentChar1,             0x194, 1,AbilityType.Additive,AbilityTypeGained.CriticalBonus),



    'Hyper Healing (Goofy)':(currentChar3, 0x1A3,1),
    'Auto Healing (Goofy)':(currentChar3, 0x1A4,1),
    'Auto Change(Goofy)' :(currentChar3, 0x1A2,1),
    'Auto Limit (Goofy)' :(currentChar3, 0x1A1,1),
    'MP Rage (Goofy)' 	:(currentChar3, 0x19C,1,AbilityType.Additive),
    'Lucky Lucky (Goofy)' :(currentChar3, 0x197,1,AbilityType.Additive),
    'Draw (Goofy)':(currentChar3, 0x195,1,AbilityType.Additive),
    'Jackpot (Goofy)':(currentChar3,0x196,1,AbilityType.Additive),
    'Item Boost (Goofy)':(currentChar3,0x19B,1,AbilityType.Additive),
    'Defender (Goofy)':(currentChar3,0x19E,1,AbilityType.Additive),
    'Damage Control (Goofy)':(currentChar3,0x21E,1,AbilityType.Additive),
    'Second Chance (Goofy)':(currentChar3,0x19F,1),
    'Once More (Goofy)':(currentChar3,0x1A0,1),

    'Draw (Donald)' :(currentChar2,0x195,1,AbilityType.Additive),
    'Lucky Lucky (Donald)' :(currentChar2,0x197,1,AbilityType.Additive),
    'MP Rage (Donald)' :(currentChar2,0x19C,1,AbilityType.Additive),
    'MP Hastera (Donald)' :(currentChar2,0x1A5,1,AbilityType.Additive),
    'Auto Limit (Donald)' :(currentChar2,0x1A1,1),
    'Hyper Healing (Donald)' :(currentChar2,0x1A3,1),
    'Auto Healing (Donald)' :(currentChar2,0x1A4,1),
    'Jackpot (Donald)' :(currentChar2,0x196,1,AbilityType.Additive),
    'Fire Boost (Donald)' :(currentChar2,0x198,1,AbilityType.Additive),
    'Blizzard Boost(Donald)' :(currentChar2,0x199,1,AbilityType.Additive),
    'Thunder Boost(Donald)' :(currentChar2,0x19A,1,AbilityType.Additive),
},
AbilityTable_enum.LevelUp : {

    'Combo Boost':(currentChar1,0x186,1,AbilityType.Additive),
    'Air Combo Boost':(currentChar1,0x187,1,AbilityType.Additive),
    'Reaction Boost':(currentChar1,0x188,1,AbilityType.Additive),
    'Finishing Plus':(currentChar1,0x189,1,AbilityType.Additive),
    'Negative Combo':(currentChar1,0x18A,1,AbilityType.Additive),
    'Berserk Charge':(currentChar1,0x18B,1),
    'Damage Drive':(currentChar1,0x18C,1,AbilityType.Additive),
    'Drive Boost':(currentChar1,0x18D,1,AbilityType.Additive),
    'Combination Boost':(currentChar1,0x190,1,AbilityType.Additive),
    'Experience Boost':(currentChar1,0x191,1,AbilityType.Additive),
    'Leaf Bracer':(currentChar1,0x192,1),
    'Magic Lock-On':(currentChar1,0x193,1),
    'Draw':(currentChar1,0x195,1,AbilityType.Additive),
    'Drive Converter':(currentChar1,0x21C,1),
    'Item Boost':(currentChar1,0x19B,1,AbilityType.Additive),
    'Defender':(currentChar1,0x19E,1,AbilityType.Additive),
    'Damage Control':(currentChar1,0x21E,1,AbilityType.Additive),
    'Second Chance':(currentChar1,0x19F,1),
    'Once More':(currentChar1,0x1A0,1),
    'Jackpot':(currentChar1,0x196,1,AbilityType.Additive),
    'Fire Boost':(currentChar1,0x198,1,AbilityType.Additive),
    'Blizzard Boost':(currentChar1,0x199,1,AbilityType.Additive),
    'Thunder Boost':(currentChar1,0x19A,1,AbilityType.Additive),

},
}