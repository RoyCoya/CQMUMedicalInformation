def GetBoneAge(standard, sex, bones):
    grade = 0
    for bone in bones: grade += Level_Grade[standard][sex][bone.name][bone.assessment]
    return next((age for age,age_range in Age_Grade[standard][sex].items() if age_range[0] <= grade <= age_range[1]), -1)

Level_Grade = {
    'RUS' : {
        'Male' : {
            'Radius' : {
                0 : 0,
                1 : 8,
                2 : 11,
                3 : 15,
                4 : 18,
                5 : 31,
                6 : 46,
                7 : 76,
                8 : 118,
                9 : 135,
                10 : 171,
                11 : 188,
                12 : 197,
                13 : 201,
                14 : 209,
            },
            'Ulna' : {
                0 : 0,
                1 : 25,
                2 : 30,
                3 : 35,
                4 : 43,
                5 : 61,
                6 : 80,
                7 : 116,
                8 : 157,
                9 : 168,
                10 : 180,
                11 : 187,
                12 : 194,
            },
            'First Metacarpal' : {
                0 : 0,
                1 : 4,
                2 : 5,
                3 : 8,
                4 : 16,
                5 : 22,
                6 : 26,
                7 : 34,
                8 : 39,
                9 : 45,
                10 : 52,
                11 : 66,
            },
            'Third Metacarpal' : {
                0 : 0,
                1 : 3,
                2 : 4,
                3 : 5,
                4 : 8,
                5 : 13,
                6 : 19,
                7 : 30,
                8 : 38,
                9 : 44,
                10 : 51,
            },
            'Fifth Metacarpal' : {
                0 : 0,
                1 : 3,
                2 : 4,
                3 : 6,
                4 : 9,
                5 : 14,
                6 : 19,
                7 : 31,
                8 : 41,
                9 : 46,
                10 : 50,
            },
            'First Proximal Phalange' : {
                0 : 0,
                1 : 4,
                2 : 5,
                3 : 7,
                4 : 11,
                5 : 17,
                6 : 23,
                7 : 29,
                8 : 36,
                9 : 44,
                10 : 52,
                11 : 59,
                12 : 66,
            },
            'Third Proximal Phalange' : {
                0 : 0,
                1 : 3,
                2 : 4,
                3 : 5,
                4 : 8,
                5 : 14,
                6 : 19,
                7 : 23,
                8 : 28,
                9 : 34,
                10 : 40,
                11 : 45,
                12 : 50,
            },
            'Fifth Proximal Phalange' : {
                0 : 0,
                1 : 3,
                2 : 4,
                3 : 6,
                4 : 10,
                5 : 16,
                6 : 19,
                7 : 24,
                8 : 28,
                9 : 33,
                10 : 40,
                11 : 44,
                12 : 50,
            },
            'Third Middle Phalange' : {
                0 : 0,
                1 : 3,
                2 : 4,
                3 : 5,
                4 : 9,
                5 : 14,
                6 : 18,
                7 : 23,
                8 : 28,
                9 : 35,
                10 : 42,
                11 : 45,
                12 : 50,
            },
            'Fifth Middle Phalange' : {
                0 : 0,
                1 : 3,
                2 : 4,
                3 : 6,
                4 : 11,
                5 : 17,
                6 : 21,
                7 : 26,
                8 : 31,
                9 : 36,
                10 : 40,
                11 : 43,
                12 : 49,
            },
            'First Distal Phalange' : {
                0 : 0,
                1 : 4,
                2 : 5,
                3 : 6,
                4 : 9,
                5 : 19,
                6 : 28,
                7 : 36,
                8 : 43,
                9 : 46,
                10 : 51,
                11 : 67,
            },
            'Third Distal Phalange' : {
                0 : 0,
                1 : 3,
                2 : 4,
                3 : 5,
                4 : 9,
                5 : 15,
                6 : 23,
                7 : 29,
                8 : 33,
                9 : 37,
                10 : 40,
                11 : 49,
            },
            'Fifth Distal Phalange' : {
                0 : 0,
                1 : 3,
                2 : 4,
                3 : 6,
                4 : 11,
                5 : 17,
                6 : 23,
                7 : 29,
                8 : 32,
                9 : 36,
                10 : 40,
                11 : 49,
            },
        },
        'Female' : {
            'Radius' : {
                0 : 0,
                1 : 10,
                2 : 15,
                3 : 22,
                4 : 25,
                5 : 40,
                6 : 59,
                7 : 91,
                8 : 125,
                9 : 138,
                10 : 178,
                11 : 192,
                12 : 199,
                13 : 203,
                14 : 210,
            },
            'Ulna' : {
                0 : 0,
                1 : 27,
                2 : 31,
                3 : 36,
                4 : 50,
                5 : 73,
                6 : 95,
                7 : 120,
                8 : 157,
                9 : 168,
                10 : 176,
                11 : 182,
                12 : 189,
            },
            'First Metacarpal' : {
                0 : 0,
                1 : 5,
                2 : 7,
                3 : 10,
                4 : 16,
                5 : 23,
                6 : 28,
                7 : 34,
                8 : 41,
                9 : 47,
                10 : 53,
                11 : 66,
            },
            'Third Metacarpal' : {
                0 : 0,
                1 : 3,
                2 : 5,
                3 : 6,
                4 : 9,
                5 : 14,
                6 : 21,
                7 : 32,
                8 : 40,
                9 : 47,
                10 : 51,
            },
            'Fifth Metacarpal' : {
                0 : 0,
                1 : 4,
                2 : 5,
                3 : 7,
                4 : 10,
                5 : 15,
                6 : 22,
                7 : 33,
                8 : 43,
                9 : 47,
                10 : 51,
            },
            'First Proximal Phalange' : {
                0 : 0,
                1 : 6,
                2 : 7,
                3 : 8,
                4 : 11,
                5 : 17,
                6 : 26,
                7 : 32,
                8 : 38,
                9 : 45,
                10 : 53,
                11 : 60,
                12 : 67,
            },
            'Third Proximal Phalange' : {
                0 : 0,
                1 : 3,
                2 : 5,
                3 : 7,
                4 : 9,
                5 : 15,
                6 : 20,
                7 : 25,
                8 : 29,
                9 : 35,
                10 : 41,
                11 : 46,
                12 : 51,
            },
            'Fifth Proximal Phalange' : {
                0 : 0,
                1 : 4,
                2 : 5,
                3 : 7,
                4 : 11,
                5 : 18,
                6 : 21,
                7 : 25,
                8 : 29,
                9 : 34,
                10 : 40,
                11 : 45,
                12 : 50,
            },
            'Third Middle Phalange' : {
                0 : 0,
                1 : 4,
                2 : 5,
                3 : 7,
                4 : 10,
                5 : 16,
                6 : 21,
                7 : 25,
                8 : 29,
                9 : 35,
                10 : 43,
                11 : 46,
                12 : 51,
            },
            'Fifth Middle Phalange' : {
                0 : 0,
                1 : 3,
                2 : 5,
                3 : 7,
                4 : 12,
                5 : 19,
                6 : 23,
                7 : 27,
                8 : 32,
                9 : 35,
                10 : 39,
                11 : 43,
                12 : 49,
            },
            'First Distal Phalange' : {
                0 : 0,
                1 : 5,
                2 : 6,
                3 : 8,
                4 : 10,
                5 : 20,
                6 : 31,
                7 : 38,
                8 : 44,
                9 : 45,
                10 : 52,
                11 : 67,
            },
            'Third Distal Phalange' : {
                0 : 0,
                1 : 3,
                2 : 5,
                3 : 7,
                4 : 10,
                5 : 16,
                6 : 24,
                7 : 30,
                8 : 33,
                9 : 36,
                10 : 39,
                11 : 49,
            },
            'Fifth Distal Phalange' : {
                0 : 0,
                1 : 5,
                2 : 6,
                3 : 7,
                4 : 11,
                5 : 18,
                6 : 25,
                7 : 29,
                8 : 33,
                9 : 35,
                10 : 39,
                11 : 49,
            },
        },
    },
    'CHN' : {
        'Male' : {
            'Radius' : {
                0 : 0,
                1 : 17,
                2 : 30,
                3 : 39,
                4 : 49,
                5 : 59,
                6 : 71,
                7 : 87,
                8 : 93,
                9 : 94,
                10 : 101,
            },
            'Capitate' : {
                0 : 0,
                1 : 8,
                2 : 18,
                3 : 37,
                4 : 58,
                5 : 75,
                6 : 80,
                7 : 129,
            },
            'Hamate' : {
                0 : 0,
                1 : 11,
                2 : 26,
                3 : 53,
                4 : 73,
                5 : 87,
                6 : 99,
                7 : 109,
                8 : 135,
            },
            'First Metacarpal' : {
                0 : 0,
                1 : 8,
                2 : 9,
                3 : 11,
                4 : 14,
                5 : 15,
                6 : 18,
                7 : 19,
                8 : 21,
            },
            'Third Metacarpal' : {
                0 : 0,
                1 : 20,
                2 : 27,
                3 : 39,
                4 : 49,
                5 : 60,
                6 : 71,
                7 : 74,
                8 : 79,
            },
            'Fifth Metacarpal' : {
                0 : 0,
                1 : 15,
                2 : 19,
                3 : 24,
                4 : 31,
                5 : 38,
                6 : 42,
                7 : 45,
                8 : 47,
            },
            'First Proximal Phalange' : {
                0 : 0,
                1 : 9,
                2 : 10,
                3 : 11,
                4 : 14,
                5 : 17,
                6 : 20,
                7 : 21,
                8 : 22,
            },
            'Third Proximal Phalange' : {
                0 : 0,
                1 : 17,
                2 : 24,
                3 : 47,
                4 : 69,
                5 : 88,
                6 : 102,
                7 : 106,
                8 : 113,
            },
            'Fifth Proximal Phalange' : {
                0 : 0,
                1 : 19,
                2 : 24,
                3 : 34,
                4 : 45,
                5 : 57,
                6 : 64,
                7 : 67,
                8 : 71,
            },
            'Third Middle Phalange' : {
                0 : 0,
                1 : 20,
                2 : 28,
                3 : 39,
                4 : 50,
                5 : 62,
                6 : 71,
                7 : 74,
                8 : 79,
            },
            'Fifth Middle Phalange' : {
                0 : 0,
                1 : 6,
                2 : 7,
                3 : 8,
                4 : 9,
                5 : 12,
                6 : 13,
                7 : 15,
                8 : 16,
            },
            'First Distal Phalange' : {
                0 : 0,
                1 : 18,
                2 : 23,
                3 : 47,
                4 : 52,
                5 : 73,
                6 : 91,
                7 : 95,
                8 : 102,
            },
            'Third Distal Phalange' : {
                0 : 0,
                1 : 20,
                2 : 25,
                3 : 34,
                4 : 42,
                5 : 49,
                6 : 61,
                7 : 63,
                8 : 68,
            },
            'Fifth Distal Phalange' : {
                0 : 0,
                1 : 7,
                2 : 8,
                3 : 9,
                4 : 11,
                5 : 13,
                6 : 15,
                7 : 16,
                8 : 17,
            },
        },
        'Female' : {
            'Radius' : {
                0 : 0,
                1 : 17,
                2 : 30,
                3 : 42,
                4 : 49,
                5 : 57,
                6 : 69,
                7 : 79,
                8 : 83,
                9 : 84,
                10 : 88,
            },
            'Capitate' : {
                0 : 0,
                1 : 3,
                2 : 14,
                3 : 39,
                4 : 53,
                5 : 63,
                6 : 72,
                7 : 100,
            },
            'Hamate' : {
                0 : 0,
                1 : 6,
                2 : 20,
                3 : 50,
                4 : 62,
                5 : 70,
                6 : 78,
                7 : 86,
                8 : 104,
            },
            'First Metacarpal' : {
                0 : 0,
                1 : 19,
                2 : 23,
                3 : 27,
                4 : 31,
                5 : 35,
                6 : 41,
                7 : 43,
                8 : 46,
            },
            'Third Metacarpal' : {
                0 : 0,
                1 : 22,
                2 : 30,
                3 : 42,
                4 : 51,
                5 : 60,
                6 : 71,
                7 : 74,
                8 : 78,
            },
            'Fifth Metacarpal' : {
                0 : 0,
                1 : 22,
                2 : 28,
                3 : 35,
                4 : 43,
                5 : 52,
                6 : 58,
                7 : 61,
                8 : 63,
            },
            'First Proximal Phalange' : {
                0 : 0,
                1 : 15,
                2 : 18,
                3 : 21,
                4 : 26,
                5 : 31,
                6 : 36,
                7 : 38,
                8 : 40,
            },
            'Third Proximal Phalange' : {
                0 : 0,
                1 : 11,
                2 : 20,
                3 : 44,
                4 : 59,
                5 : 73,
                6 : 84,
                7 : 88,
                8 : 93,
            },
            'Fifth Proximal Phalange' : {
                0 : 0,
                1 : 21,
                2 : 29,
                3 : 43,
                4 : 53,
                5 : 65,
                6 : 73,
                7 : 77,
                8 : 80,
            },
            'Third Middle Phalange' : {
                0 : 0,
                1 : 20,
                2 : 31,
                3 : 43,
                4 : 53,
                5 : 64,
                6 : 73,
                7 : 77,
                8 : 80,
            },
            'Fifth Middle Phalange' : {
                0 : 0,
                1 : 16,
                2 : 19,
                3 : 23,
                4 : 28,
                5 : 33,
                6 : 36,
                7 : 37,
                8 : 39,
            },
            'First Distal Phalange' : {
                0 : 0,
                1 : 15,
                2 : 19,
                3 : 44,
                4 : 54,
                5 : 63,
                6 : 77,
                7 : 81,
                8 : 86,
            },
            'Third Distal Phalange' : {
                0 : 0,
                1 : 22,
                2 : 28,
                3 : 39,
                4 : 46,
                5 : 53,
                6 : 65,
                7 : 67,
                8 : 71,
            },
            'Fifth Distal Phalange' : {
                0 : 0,
                1 : 13,
                2 : 15,
                3 : 19,
                4 : 22,
                5 : 26,
                6 : 29,
                7 : 31,
                8 : 32,
            },
        },
    },
}

Age_Grade = {
    'RUS' : {
        'Male' : {
            0.0 : [0, 0],
            0.1 : [1, 1],
            0.2 : [2, 2],
            0.3 : [3, 3],
            0.4 : [4, 5],
            0.5 : [6, 7],
            0.6 : [8, 9],
            0.7 : [10, 11],
            0.8 : [12, 13],
            0.9 : [14, 15],
            1.0 : [16, 17],
            1.1 : [18, 19],
            1.2 : [20, 22],
            1.3 : [23, 24],
            1.4 : [25, 27],
            1.5 : [28, 29],
            1.6 : [30, 31],
            1.7 : [32, 33],
            1.8 : [34, 35],
            1.9 : [36, 38],
            2.0 : [39, 40],
            2.1 : [41, 42],
            2.2 : [43, 44],
            2.3 : [45, 47],
            2.4 : [48, 49],
            2.5 : [50, 51],
            2.6 : [52, 54],
            2.7 : [55, 56],
            2.8 : [57, 59],
            2.9 : [60, 62],
            3.0 : [63, 63],
            3.1 : [64, 64],
            3.2 : [65, 65],
            3.3 : [66, 66],
            3.4 : [67, 67],
            3.5 : [68, 68],
            3.6 : [69, 69],
            3.7 : [70, 71],
            3.8 : [72, 72],
            3.9 : [73, 74],
            4.0 : [75, 75],
            4.2 : [76, 76],
            4.4 : [77, 77],
            4.5 : [78, 78],
            4.6 : [79, 79],
            4.7 : [80, 80],
            4.8 : [81, 81],
            4.9 : [82, 83],
            5.0 : [84, 84],
            5.1 : [85, 85],
            5.2 : [86, 87],
            5.3 : [88, 88],
            5.4 : [89, 90],
            5.5 : [91, 91],
            5.6 : [92, 93],
            5.7 : [94, 95],
            5.8 : [96, 97],
            5.9 : [98, 99],
            6.0 : [100, 100],
            6.1 : [101, 101],
            6.2 : [102, 102],
            6.3 : [103, 103],
            6.4 : [104, 105],
            6.5 : [106, 108],
            6.6 : [109, 109],
            6.7 : [110, 111],
            6.8 : [112, 113],
            6.9 : [114, 115],
            7.0 : [116, 117],
            7.1 : [118, 119],
            7.2 : [120, 122],
            7.3 : [123, 124],
            7.4 : [125, 127],
            7.5 : [128, 130],
            7.6 : [131, 133],
            7.7 : [134, 137],
            7.8 : [138, 139],
            7.9 : [140, 142],
            8.0 : [143, 146],
            8.1 : [147, 152],
            8.2 : [153, 156],
            8.3 : [157, 159],
            8.4 : [160, 164],
            8.5 : [165, 168],
            8.6 : [169, 173],
            8.7 : [174, 181],
            8.8 : [182, 183],
            8.9 : [184, 191],
            9.0 : [192, 192],
            9.1 : [193, 199],
            9.2 : [200, 201],
            9.3 : [202, 204],
            9.4 : [205, 209],
            9.5 : [210, 215],
            9.6 : [216, 220],
            9.7 : [221, 225],
            9.8 : [226, 231],
            9.9 : [232, 237],
            10.0 : [238, 242],
            10.1 : [243, 251],
            10.2 : [252, 254],
            10.3 : [255, 260],
            10.4 : [261, 266],
            10.5 : [267, 273],
            10.6 : [274, 282],
            10.7 : [283, 290],
            10.8 : [291, 295],
            10.9 : [296, 303],
            11.0 : [304, 312],
            11.1 : [313, 321],
            11.2 : [322, 330],
            11.3 : [331, 339],
            11.4 : [340, 348],
            11.5 : [349, 358],
            11.6 : [359, 369],
            11.7 : [370, 380],
            11.8 : [381, 394],
            11.9 : [395, 402],
            12.0 : [403, 414],
            12.1 : [415, 427],
            12.2 : [428, 439],
            12.3 : [440, 454],
            12.4 : [455, 468],
            12.5 : [469, 479],
            12.6 : [480, 493],
            12.7 : [494, 508],
            12.8 : [509, 519],
            12.9 : [520, 538],
            13.0 : [539, 548],
            13.1 : [549, 565],
            13.2 : [566, 581],
            13.3 : [582, 596],
            13.4 : [597, 614],
            13.5 : [615, 630],
            13.6 : [631, 641],
            13.7 : [642, 655],
            13.8 : [656, 671],
            13.9 : [672, 685],
            14.0 : [686, 699],
            14.1 : [700, 714],
            14.2 : [715, 728],
            14.3 : [729, 743],
            14.4 : [744, 759],
            14.5 : [760, 776],
            14.6 : [777, 791],
            14.7 : [792, 807],
            14.8 : [808, 827],
            14.9 : [828, 842],
            15.0 : [843, 853],
            15.1 : [854, 865],
            15.2 : [866, 882],
            15.3 : [883, 891],
            15.4 : [892, 900],
            15.5 : [901, 911],
            15.6 : [912, 919],
            15.7 : [920, 923],
            15.8 : [924, 929],
            15.9 : [930, 935],
            16.0 : [936, 939],
            16.1 : [940, 940],
            16.2 : [941, 942],
            16.3 : [943, 950],
            16.4 : [951, 951],
            16.5 : [952, 952],
            16.6 : [953, 953],
            16.7 : [954, 954],
            16.8 : [955, 955],
            16.9 : [956, 957],
            17.0 : [958, 958],
            17.1 : [959, 960],
            17.2 : [961, 962],
            17.3 : [963, 963],
            17.4 : [964, 966],
            17.5 : [967, 980],
            17.6 : [981, 984],
            17.7 : [985, 997],
            17.8 : [998, 998],
            17.9 : [997, 997],
            18.0 : [997, 1000],
        },
        'Female' : {
            0.0 : [0, 2],
            0.1 : [3, 5],
            0.2 : [6, 8],
            0.3 : [9, 11],
            0.4 : [11, 15],
            0.5 : [16, 21],
            0.6 : [22, 25],
            0.7 : [26, 29],
            0.8 : [30, 34],
            0.9 : [35, 41],
            1.0 : [42, 45],
            1.1 : [46, 49],
            1.2 : [50, 53],
            1.3 : [54, 58],
            1.4 : [59, 62],
            1.5 : [63, 65],
            1.6 : [66, 68],
            1.7 : [69, 72],
            1.8 : [73, 74],
            1.9 : [75, 77],
            2.0 : [78, 79],
            2.1 : [80, 81],
            2.2 : [82, 83],
            2.3 : [84, 85],
            2.4 : [86, 88],
            2.5 : [89, 90],
            2.6 : [91, 92],
            2.7 : [93, 94],
            2.8 : [95, 96],
            2.9 : [97, 99],
            3.0 : [100, 100],
            3.1 : [101, 101],
            3.2 : [102, 103],
            3.3 : [104, 104],
            3.4 : [105, 106],
            3.5 : [107, 107],
            3.6 : [108, 109],
            3.7 : [110, 111],
            3.8 : [112, 113],
            3.9 : [114, 115],
            4.0 : [116, 116],
            4.1 : [117, 117],
            4.2 : [118, 118],
            4.3 : [119, 119],
            4.4 : [120, 120],
            4.5 : [121, 122],
            4.6 : [123, 123],
            4.7 : [124, 125],
            4.8 : [126, 127],
            4.9 : [128, 129],
            5.0 : [130, 132],
            5.1 : [133, 135],
            5.2 : [136, 138],
            5.3 : [139, 141],
            5.4 : [142, 145],
            5.5 : [146, 149],
            5.6 : [150, 152],
            5.7 : [153, 154],
            5.8 : [155, 157],
            5.9 : [158, 161],
            6.0 : [162, 165],
            6.1 : [166, 169],
            6.2 : [170, 174],
            6.3 : [175, 178],
            6.4 : [179, 183],
            6.5 : [184, 188],
            6.6 : [189, 193],
            6.7 : [194, 198],
            6.8 : [199, 203],
            6.9 : [204, 208],
            7.0 : [209, 213],
            7.1 : [214, 219],
            7.2 : [220, 224],
            7.3 : [225, 230],
            7.4 : [231, 237],
            7.5 : [238, 242],
            7.6 : [243, 248],
            7.7 : [249, 254],
            7.8 : [255, 260],
            7.9 : [261, 266],
            8.0 : [267, 274],
            8.1 : [275, 282],
            8.2 : [283, 290],
            8.3 : [291, 298],
            8.4 : [299, 306],
            8.5 : [307, 314],
            8.6 : [315, 323],
            8.7 : [324, 331],
            8.8 : [332, 341],
            8.9 : [342, 349],
            9.0 : [350, 359],
            9.1 : [360, 369],
            9.2 : [370, 380],
            9.3 : [381, 389],
            9.4 : [390, 399],
            9.5 : [400, 409],
            9.6 : [410, 420],
            9.7 : [421, 430],
            9.8 : [431, 441],
            9.9 : [442, 452],
            10.0 : [453, 462],
            10.1 : [463, 473],
            10.2 : [474, 484],
            10.3 : [485, 495],
            10.4 : [496, 506],
            10.5 : [507, 519],
            10.6 : [520, 531],
            10.7 : [532, 544],
            10.8 : [545, 557],
            10.9 : [558, 570],
            11.0 : [571, 583],
            11.1 : [584, 596],
            11.2 : [597, 609],
            11.3 : [610, 622],
            11.4 : [623, 635],
            11.5 : [636, 647],
            11.6 : [648, 659],
            11.7 : [660, 672],
            11.8 : [673, 683],
            11.9 : [684, 701],
            12.0 : [702, 712],
            12.1 : [713, 727],
            12.2 : [728, 748],
            12.3 : [749, 761],
            12.4 : [762, 779],
            12.5 : [780, 789],
            12.6 : [790, 808],
            12.7 : [809, 819],
            12.8 : [820, 835],
            12.9 : [836, 851],
            13.0 : [852, 860],
            13.1 : [861, 872],
            13.2 : [873, 885],
            13.3 : [886, 894],
            13.4 : [895, 906],
            13.5 : [907, 913],
            13.6 : [914, 926],
            13.7 : [927, 929],
            13.8 : [930, 934],
            13.9 : [935, 942],
            14.0 : [943, 944],
            14.1 : [945, 952],
            14.2 : [953, 954],
            14.3 : [955, 959],
            14.4 : [960, 962],
            14.5 : [963, 966],
            14.6 : [967, 967],
            14.7 : [968, 969],
            14.8 : [970, 974],
            14.9 : [975, 975],
            15.0 : [976, 977],
            15.1 : [978, 979],
            15.2 : [980, 981],
            15.3 : [982, 982],
            15.4 : [983, 985],
            15.5 : [986, 986],
            15.7 : [987, 987],
            15.9 : [988, 988],
            16.1 : [989, 989],
            16.2 : [990, 990],
            16.3 : [991, 991],
            16.4 : [992, 992],
            16.5 : [993, 993],
            16.6 : [994, 994],
            16.7 : [995, 996],
            16.8 : [997, 997],
            16.9 : [998, 999],
            17.0 : [1000, 1000],
        },
    },
    'CHN' : {
        'Male' : {
            0.0 : [0.0, 13.0],
            0.1 : [14.0, 22.0],
            0.2 : [23.0, 29.0],
            0.3 : [30.0, 36.0],
            0.4 : [37.0, 42.0],
            0.5 : [43.0, 44.0],
            0.6 : [45.0, 46.0],
            0.7 : [47.0, 50.0],
            0.8 : [51.0, 54.0],
            0.9 : [55.0, 60.0],
            1.0 : [61.0, 75.0],
            1.1 : [76.0, 92.0],
            1.2 : [93.0, 110.0],
            1.3 : [111.0, 130.0],
            1.4 : [131.0, 151.0],
            1.5 : [152.0, 168.0],
            1.6 : [169.0, 185.0],
            1.7 : [186.0, 202.0],
            1.8 : [203.0, 219.0],
            1.9 : [220.0, 235.0],
            2.0 : [236.0, 252.0],
            2.1 : [253.0, 269.0],
            2.2 : [270.0, 286.0],
            2.3 : [287.0, 302.0],
            2.4 : [303.0, 318.0],
            2.5 : [319.0, 332.0],
            2.6 : [333.0, 345.0],
            2.7 : [346.0, 357.0],
            2.8 : [358.0, 369.0],
            2.9 : [370.0, 379.0],
            3.0 : [380.0, 389.0],
            3.1 : [390.0, 398.0],
            3.2 : [399.0, 406.0],
            3.3 : [407.0, 414.0],
            3.4 : [415.0, 421.0],
            3.5 : [422.0, 428.0],
            3.6 : [429.0, 435.0],
            3.7 : [436.0, 441.0],
            3.8 : [442.0, 447.0],
            3.9 : [448.0, 452.0],
            4.0 : [453.0, 456.0],
            4.1 : [457.0, 460.0],
            4.2 : [461.0, 464.0],
            4.3 : [465.0, 467.0],
            4.4 : [468.0, 471.0],
            4.5 : [472.0, 475.0],
            4.6 : [476.0, 480.0],
            4.7 : [481.0, 484.0],
            4.8 : [485.0, 489.0],
            4.9 : [489.0, 494.0],
            5.0 : [495.0, 497.0],
            5.1 : [498.0, 501.0],
            5.2 : [502.0, 505.0],
            5.3 : [506.0, 509.0],
            5.4 : [510.0, 513.0],
            5.5 : [514.0, 517.0],
            5.6 : [518.0, 520.0],
            5.7 : [521.0, 524.0],
            5.8 : [525.0, 528.0],
            5.9 : [529.0, 531.0],
            6.0 : [532.0, 535.0],
            6.1 : [536.0, 539.0],
            6.2 : [540.0, 543.0],
            6.3 : [544.0, 547.0],
            6.4 : [548.0, 551.0],
            6.5 : [552.0, 555.0],
            6.6 : [556.0, 559.0],
            6.7 : [560.0, 563.0],
            6.8 : [564.0, 566.0],
            6.9 : [567.0, 570.0],
            7.0 : [571.0, 573.0],
            7.1 : [574.0, 576.0],
            7.2 : [577.0, 579.0],
            7.3 : [580.0, 582.0],
            7.4 : [583.0, 585.0],
            7.5 : [586.0, 588.0],
            7.6 : [589.0, 590.0],
            7.7 : [591.0, 593.0],
            7.8 : [594.0, 596.0],
            7.9 : [597.0, 598.0],
            8.0 : [599.0, 602.0],
            8.1 : [603.0, 605.0],
            8.2 : [606.0, 609.0],
            8.3 : [610.0, 612.0],
            8.4 : [613.0, 615.0],
            8.5 : [616.0, 618.0],
            8.6 : [619.0, 621.0],
            8.7 : [622.0, 624.0],
            8.8 : [625.0, 627.0],
            8.9 : [628.0, 630.0],
            9.0 : [631.0, 632.0],
            9.1 : [633.0, 634.0],
            9.2 : [635.0, 636.0],
            9.3 : [637.0, 637.0],
            9.4 : [638.0, 639.0],
            9.5 : [640.0, 641.0],
            9.6 : [642.0, 643.0],
            9.7 : [644.0, 645.0],
            9.8 : [646.0, 647.0],
            9.9 : [648.0, 649.0],
            10.0 : [650.0, 653.0],
            10.1 : [654.0, 656.0],
            10.2 : [657.0, 660.0],
            10.3 : [661.0, 664.0],
            10.4 : [665.0, 668.0],
            10.5 : [669.0, 672.0],
            10.6 : [673.0, 676.0],
            10.7 : [677.0, 681.0],
            10.8 : [682.0, 685.0],
            10.9 : [686.0, 690.0],
            11.0 : [691.0, 693.0],
            11.1 : [694.0, 697.0],
            11.2 : [698.0, 701.0],
            11.3 : [702.0, 705.0],
            11.4 : [706.0, 710.0],
            11.5 : [711.0, 715.0],
            11.6 : [716.0, 720.0],
            11.7 : [721.0, 725.0],
            11.8 : [726.0, 731.0],
            11.9 : [732.0, 737.0],
            12.0 : [738.0, 744.0],
            12.1 : [745.0, 752.0],
            12.2 : [753.0, 760.0],
            12.3 : [761.0, 769.0],
            12.4 : [770.0, 778.0],
            12.5 : [779.0, 787.0],
            12.6 : [788.0, 797.0],
            12.7 : [798.0, 807.0],
            12.8 : [808.0, 817.0],
            12.9 : [818.0, 827.0],
            13.0 : [828.0, 839.0],
            13.1 : [840.0, 850.0],
            13.2 : [851.0, 861.0],
            13.3 : [862.0, 872.0],
            13.4 : [873.0, 882.0],
            13.5 : [883.0, 891.0],
            13.6 : [892.0, 900.0],
            13.7 : [901.0, 907.0],
            13.8 : [908.0, 913.0],
            13.9 : [914.0, 918.0],
            14.0 : [919.0, 920.0],
            14.1 : [921.0, 921.0],
            14.2 : [922.0, 922.0],
            14.4 : [923.0, 923.0],
            14.6 : [924.0, 924.0],
            14.7 : [925.0, 926.0],
            14.8 : [927.0, 928.0],
            14.9 : [929.0, 930.0],
            15.0 : [931.0, 935.0],
            15.1 : [936.0, 939.0],
            15.2 : [940.0, 944.0],
            15.3 : [945.0, 949.0],
            15.4 : [950.0, 954.0],
            15.5 : [955.0, 959.0],
            15.6 : [960.0, 963.0],
            15.7 : [964.0, 968.0],
            15.8 : [969.0, 973.0],
            15.9 : [974.0, 978.0],
            16.0 : [979.0, 981.0],
            16.1 : [982.0, 984.0],
            16.2 : [985.0, 986.0],
            16.3 : [987.0, 988.0],
            16.4 : [989.0, 989.0],
            16.5 : [990.0, 990.0],
            16.8 : [991.0, 991.0],
            17.0 : [992.0, 992.0],
            17.6 : [993.0, 993.0],
            18.4 : [994.0, 1000],
        },
        'Female' : {
            0.0 : [0.0, 4.0],
            0.1 : [5.0, 10.0],
            0.2 : [11.0, 16.0],
            0.3 : [17.0, 24.0],
            0.4 : [25.0, 33.0],
            0.5 : [34.0, 39.0],
            0.6 : [40.0, 49.0],
            0.7 : [50.0, 62.0],
            0.8 : [63.0, 80.0],
            0.9 : [81.0, 101.0],
            1.0 : [102.0, 144.0],
            1.1 : [145.0, 188.0],
            1.2 : [189.0, 234.0],
            1.3 : [235.0, 280.0],
            1.4 : [281.0, 328.0],
            1.5 : [329.0, 360.0],
            1.6 : [361.0, 389.0],
            1.7 : [390.0, 414.0],
            1.8 : [415.0, 436.0],
            1.9 : [437.0, 454.0],
            2.0 : [455.0, 469.0],
            2.1 : [470.0, 481.0],
            2.2 : [482.0, 491.0],
            2.3 : [492.0, 499.0],
            2.4 : [500.0, 504.0],
            2.5 : [505.0, 510.0],
            2.6 : [511.0, 515.0],
            2.7 : [516.0, 520.0],
            2.8 : [521.0, 526.0],
            2.9 : [527.0, 531.0],
            3.0 : [532.0, 534.0],
            3.1 : [535.0, 538.0],
            3.2 : [539.0, 541.0],
            3.3 : [542.0, 543.0],
            3.4 : [544.0, 546.0],
            3.5 : [547.0, 548.0],
            3.6 : [549.0, 551.0],
            3.7 : [552.0, 553.0],
            3.8 : [554.0, 555.0],
            3.9 : [556.0, 557.0],
            4.0 : [558.0, 561.0],
            4.1 : [562.0, 565.0],
            4.2 : [566.0, 570.0],
            4.3 : [571.0, 574.0],
            4.4 : [575.0, 579.0],
            4.5 : [580.0, 582.0],
            4.6 : [583.0, 584.0],
            4.7 : [585.0, 587.0],
            4.8 : [588.0, 590.0],
            4.9 : [591.0, 593.0],
            5.0 : [594.0, 596.0],
            5.1 : [597.0, 600.0],
            5.2 : [601.0, 604.0],
            5.3 : [605.0, 607.0],
            5.4 : [608.0, 611.0],
            5.5 : [612.0, 615.0],
            5.6 : [616.0, 619.0],
            5.7 : [620.0, 622.0],
            5.8 : [623.0, 626.0],
            5.9 : [627.0, 630.0],
            6.0 : [631.0, 633.0],
            6.1 : [634.0, 636.0],
            6.2 : [637.0, 639.0],
            6.3 : [640.0, 641.0],
            6.4 : [642.0, 644.0],
            6.5 : [645.0, 646.0],
            6.6 : [647.0, 649.0],
            6.7 : [650.0, 651.0],
            6.8 : [652.0, 653.0],
            6.9 : [654.0, 656.0],
            7.0 : [657.0, 658.0],
            7.1 : [659.0, 660.0],
            7.2 : [661.0, 662.0],
            7.3 : [663.0, 663.0],
            7.4 : [664.0, 667.0],
            7.5 : [668.0, 669.0],
            7.6 : [670.0, 671.0],
            7.7 : [672.0, 674.0],
            7.8 : [675.0, 676.0],
            7.9 : [677.0, 679.0],
            8.0 : [680.0, 681.0],
            8.1 : [682.0, 683.0],
            8.2 : [684.0, 686.0],
            8.3 : [687.0, 689.0],
            8.4 : [690.0, 693.0],
            8.5 : [694.0, 696.0],
            8.6 : [697.0, 700.0],
            8.7 : [701.0, 704.0],
            8.8 : [705.0, 708.0],
            8.9 : [709.0, 713.0],
            9.0 : [714.0, 720.0],
            9.1 : [721.0, 727.0],
            9.2 : [728.0, 734.0],
            9.3 : [735.0, 742.0],
            9.4 : [743.0, 749.0],
            9.5 : [750.0, 756.0],
            9.6 : [757.0, 762.0],
            9.7 : [763.0, 769.0],
            9.8 : [770.0, 776.0],
            9.9 : [777.0, 783.0],
            10.0 : [784.0, 784.0],
            10.1 : [785.0, 787.0],
            10.2 : [788.0, 790.0],
            10.3 : [791.0, 794.0],
            10.4 : [795.0, 798.0],
            10.5 : [799.0, 808.0],
            10.6 : [809.0, 819.0],
            10.7 : [820.0, 830.0],
            10.8 : [831.0, 843.0],
            10.9 : [844.0, 855.0],
            11.0 : [856.0, 866.0],
            11.1 : [867.0, 875.0],
            11.2 : [876.0, 885.0],
            11.3 : [886.0, 893.0],
            11.4 : [894.0, 901.0],
            11.5 : [902.0, 907.0],
            11.6 : [908.0, 913.0],
            11.7 : [914.0, 918.0],
            11.8 : [919.0, 922.0],
            11.9 : [923.0, 926.0],
            12.0 : [927.0, 927.0],
            12.2 : [928.0, 929.0],
            12.6 : [930.0, 931.0],
            12.7 : [932.0, 934.0],
            12.8 : [935.0, 937.0],
            12.9 : [938.0, 940.0],
            13.0 : [941.0, 943.0],
            13.1 : [944.0, 947.0],
            13.2 : [948.0, 950.0],
            13.3 : [951.0, 953.0],
            13.4 : [954.0, 957.0],
            13.5 : [958.0, 960.0],
            13.6 : [961.0, 964.0],
            13.7 : [965.0, 967.0],
            13.8 : [968.0, 970.0],
            13.9 : [971.0, 973.0],
            14.0 : [974.0, 976.0],
            14.1 : [977.0, 978.0],
            14.2 : [979.0, 980.0],
            14.3 : [981.0, 982.0],
            14.4 : [983.0, 984.0],
            14.5 : [985.0, 986.0],
            14.6 : [987.0, 987.0],
            14.7 : [988.0, 989.0],
            14.8 : [990.0, 990.0],
            14.9 : [991.0, 991.0],
            15.2 : [992.0, 992.0],
            15.4 : [993.0, 993.0],
            15.7 : [994.0, 994.0],
            15.9 : [995.0, 995.0],
            16.3 : [996.0, 996.0],
            17.2 : [997.0, 999.0],
            17.3 : [1000.0, 1000.0],
        },
    },
}