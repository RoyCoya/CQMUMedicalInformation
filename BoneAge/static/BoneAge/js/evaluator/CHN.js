/* CHN等级、分数、年龄转换表 */
var grade_to_age = {
    'male' : {
        0 : {"min": 0, "max": 13},
        0.1 : {"min": 14, "max": 22},
        0.2 : {"min": 23, "max": 29},
        0.3 : {"min": 30, "max": 36},
        0.4 : {"min": 37, "max": 42},
        0.5 : {"min": 43, "max": 44},
        0.6 : {"min": 45, "max": 46},
        0.7 : {"min": 47, "max": 50},
        0.8 : {"min": 51, "max": 54},
        0.9 : {"min": 55, "max": 60},
        1 : {"min": 61, "max": 75},
        1.1 : {"min": 76, "max": 92},
        1.2 : {"min": 93, "max": 110},
        1.3 : {"min": 111, "max": 130},
        1.4 : {"min": 131, "max": 151},
        1.5 : {"min": 152, "max": 168},
        1.6 : {"min": 169, "max": 185},
        1.7 : {"min": 186, "max": 202},
        1.8 : {"min": 203, "max": 219},
        1.9 : {"min": 220, "max": 235},
        2 : {"min": 236, "max": 252},
        2.1 : {"min": 253, "max": 269},
        2.2 : {"min": 270, "max": 286},
        2.3 : {"min": 287, "max": 302},
        2.4 : {"min": 303, "max": 318},
        2.5 : {"min": 319, "max": 332},
        2.6 : {"min": 333, "max": 345},
        2.7 : {"min": 346, "max": 357},
        2.8 : {"min": 358, "max": 369},
        2.9 : {"min": 370, "max": 379},
        3 : {"min": 380, "max": 389},
        3.1 : {"min": 390, "max": 398},
        3.2 : {"min": 399, "max": 406},
        3.3 : {"min": 407, "max": 414},
        3.4 : {"min": 415, "max": 421},
        3.5 : {"min": 422, "max": 428},
        3.6 : {"min": 429, "max": 435},
        3.7 : {"min": 436, "max": 441},
        3.8 : {"min": 442, "max": 447},
        3.9 : {"min": 448, "max": 452},
        4 : {"min": 453, "max": 456},
        4.1 : {"min": 457, "max": 460},
        4.2 : {"min": 461, "max": 464},
        4.3 : {"min": 465, "max": 467},
        4.4 : {"min": 468, "max": 471},
        4.5 : {"min": 472, "max": 475},
        4.6 : {"min": 476, "max": 480},
        4.7 : {"min": 481, "max": 484},
        4.8 : {"min": 485, "max": 489},
        4.9 : {"min": 490, "max": 494},
        5 : {"min": 495, "max": 497},
        5.1 : {"min": 498, "max": 501},
        5.2 : {"min": 502, "max": 505},
        5.3 : {"min": 506, "max": 509},
        5.4 : {"min": 510, "max": 513},
        5.5 : {"min": 514, "max": 517},
        5.6 : {"min": 518, "max": 520},
        5.7 : {"min": 521, "max": 524},
        5.8 : {"min": 525, "max": 528},
        5.9 : {"min": 529, "max": 531},
        6 : {"min": 532, "max": 535},
        6.1 : {"min": 536, "max": 539},
        6.2 : {"min": 540, "max": 543},
        6.3 : {"min": 544, "max": 547},
        6.4 : {"min": 548, "max": 551},
        6.5 : {"min": 552, "max": 555},
        6.6 : {"min": 556, "max": 559},
        6.7 : {"min": 560, "max": 563},
        6.8 : {"min": 564, "max": 566},
        6.9 : {"min": 567, "max": 570},
        7 : {"min": 571, "max": 573},
        7.1 : {"min": 574, "max": 576},
        7.2 : {"min": 577, "max": 579},
        7.3 : {"min": 580, "max": 582},
        7.4 : {"min": 583, "max": 585},
        7.5 : {"min": 586, "max": 588},
        7.6 : {"min": 589, "max": 590},
        7.7 : {"min": 591, "max": 593},
        7.8 : {"min": 594, "max": 596},
        7.9 : {"min": 597, "max": 598},
        8 : {"min": 599, "max": 602},
        8.1 : {"min": 603, "max": 605},
        8.2 : {"min": 606, "max": 609},
        8.3 : {"min": 610, "max": 612},
        8.4 : {"min": 613, "max": 615},
        8.5 : {"min": 616, "max": 618},
        8.6 : {"min": 619, "max": 621},
        8.7 : {"min": 622, "max": 624},
        8.8 : {"min": 625, "max": 627},
        8.9 : {"min": 628, "max": 630},
        9 : {"min": 631, "max": 632},
        9.1 : {"min": 633, "max": 634},
        9.2 : {"min": 635, "max": 636},
        9.3 : {"min": 637, "max": 637},
        9.4 : {"min": 638, "max": 639},
        9.5 : {"min": 640, "max": 641},
        9.6 : {"min": 642, "max": 643},
        9.7 : {"min": 644, "max": 645},
        9.8 : {"min": 646, "max": 647},
        9.9 : {"min": 648, "max": 649},
        10 : {"min": 650, "max": 653},
        10.1 : {"min": 654, "max": 656},
        10.2 : {"min": 657, "max": 660},
        10.3 : {"min": 661, "max": 664},
        10.4 : {"min": 665, "max": 668},
        10.5 : {"min": 669, "max": 672},
        10.6 : {"min": 673, "max": 676},
        10.7 : {"min": 677, "max": 681},
        10.8 : {"min": 682, "max": 685},
        10.9 : {"min": 686, "max": 690},
        11 : {"min": 691, "max": 693},
        11.1 : {"min": 694, "max": 697},
        11.2 : {"min": 698, "max": 701},
        11.3 : {"min": 702, "max": 705},
        11.4 : {"min": 706, "max": 710},
        11.5 : {"min": 711, "max": 715},
        11.6 : {"min": 716, "max": 720},
        11.7 : {"min": 721, "max": 725},
        11.8 : {"min": 726, "max": 731},
        11.9 : {"min": 732, "max": 737},
        12 : {"min": 738, "max": 744},
        12.1 : {"min": 745, "max": 752},
        12.2 : {"min": 753, "max": 760},
        12.3 : {"min": 761, "max": 769},
        12.4 : {"min": 770, "max": 778},
        12.5 : {"min": 779, "max": 787},
        12.6 : {"min": 788, "max": 797},
        12.7 : {"min": 798, "max": 807},
        12.8 : {"min": 808, "max": 817},
        12.9 : {"min": 818, "max": 827},
        13 : {"min": 828, "max": 839},
        13.1 : {"min": 840, "max": 850},
        13.2 : {"min": 851, "max": 861},
        13.3 : {"min": 862, "max": 872},
        13.4 : {"min": 873, "max": 882},
        13.5 : {"min": 883, "max": 891},
        13.6 : {"min": 892, "max": 900},
        13.7 : {"min": 901, "max": 907},
        13.8 : {"min": 908, "max": 913},
        13.9 : {"min": 914, "max": 918},
        14 : {"min": 919, "max": 920},
        14.1 : {"min": 921, "max": 921},
        14.2 : {"min": 922, "max": 922},
        14.4 : {"min": 923, "max": 923},
        14.6 : {"min": 924, "max": 924},
        14.7 : {"min": 925, "max": 926},
        14.8 : {"min": 927, "max": 928},
        14.9 : {"min": 929, "max": 930},
        15 : {"min": 931, "max": 935},
        15.1 : {"min": 936, "max": 939},
        15.2 : {"min": 940, "max": 944},
        15.3 : {"min": 945, "max": 949},
        15.4 : {"min": 950, "max": 954},
        15.5 : {"min": 955, "max": 959},
        15.6 : {"min": 960, "max": 963},
        15.7 : {"min": 964, "max": 968},
        15.8 : {"min": 969, "max": 973},
        15.9 : {"min": 974, "max": 978},
        16 : {"min": 979, "max": 981},
        16.1 : {"min": 982, "max": 984},
        16.2 : {"min": 985, "max": 986},
        16.3 : {"min": 987, "max": 988},
        16.4 : {"min": 989, "max": 989},
        16.5 : {"min": 990, "max": 990},
        16.8 : {"min": 991, "max": 991},
        17 : {"min": 992, "max": 992},
        17.6 : {"min": 993, "max": 999},
        18.4 : {"min": 999, "max": 1000},
    },
    'female' : {
        0 : {"min": 0, "max": 4},
        0.1 : {"min": 5, "max": 10},
        0.2 : {"min": 11, "max": 16},
        0.3 : {"min": 17, "max": 24},
        0.4 : {"min": 25, "max": 33},
        0.5 : {"min": 34, "max": 39},
        0.6 : {"min": 40, "max": 49},
        0.7 : {"min": 50, "max": 62},
        0.8 : {"min": 63, "max": 80},
        0.9 : {"min": 81, "max": 101},
        1 : {"min": 102, "max": 144},
        1.1 : {"min": 145, "max": 188},
        1.2 : {"min": 189, "max": 234},
        1.3 : {"min": 235, "max": 280},
        1.4 : {"min": 281, "max": 328},
        1.5 : {"min": 329, "max": 360},
        1.6 : {"min": 361, "max": 389},
        1.7 : {"min": 390, "max": 414},
        1.8 : {"min": 415, "max": 436},
        1.9 : {"min": 437, "max": 454},
        2 : {"min": 455, "max": 469},
        2.1 : {"min": 470, "max": 481},
        2.2 : {"min": 482, "max": 491},
        2.3 : {"min": 492, "max": 499},
        2.4 : {"min": 500, "max": 504},
        2.5 : {"min": 505, "max": 510},
        2.6 : {"min": 511, "max": 515},
        2.7 : {"min": 516, "max": 520},
        2.8 : {"min": 521, "max": 526},
        2.9 : {"min": 527, "max": 531},
        3 : {"min": 532, "max": 534},
        3.1 : {"min": 535, "max": 538},
        3.2 : {"min": 539, "max": 541},
        3.3 : {"min": 542, "max": 543},
        3.4 : {"min": 544, "max": 546},
        3.5 : {"min": 547, "max": 548},
        3.6 : {"min": 549, "max": 551},
        3.7 : {"min": 552, "max": 553},
        3.8 : {"min": 554, "max": 555},
        3.9 : {"min": 556, "max": 557},
        4 : {"min": 558, "max": 561},
        4.1 : {"min": 562, "max": 565},
        4.2 : {"min": 566, "max": 570},
        4.3 : {"min": 571, "max": 574},
        4.4 : {"min": 575, "max": 579},
        4.5 : {"min": 580, "max": 582},
        4.6 : {"min": 583, "max": 584},
        4.7 : {"min": 585, "max": 587},
        4.8 : {"min": 588, "max": 590},
        4.9 : {"min": 591, "max": 593},
        5 : {"min": 594, "max": 596},
        5.1 : {"min": 597, "max": 600},
        5.2 : {"min": 601, "max": 604},
        5.3 : {"min": 605, "max": 607},
        5.4 : {"min": 608, "max": 611},
        5.5 : {"min": 612, "max": 615},
        5.6 : {"min": 616, "max": 619},
        5.7 : {"min": 620, "max": 622},
        5.8 : {"min": 623, "max": 626},
        5.9 : {"min": 627, "max": 630},
        6 : {"min": 631, "max": 633},
        6.1 : {"min": 634, "max": 636},
        6.2 : {"min": 637, "max": 639},
        6.3 : {"min": 640, "max": 641},
        6.4 : {"min": 642, "max": 644},
        6.5 : {"min": 645, "max": 646},
        6.6 : {"min": 647, "max": 649},
        6.7 : {"min": 650, "max": 651},
        6.8 : {"min": 652, "max": 653},
        6.9 : {"min": 654, "max": 656},
        7 : {"min": 657, "max": 658},
        7.1 : {"min": 659, "max": 660},
        7.2 : {"min": 661, "max": 662},
        7.3 : {"min": 663, "max": 663},
        7.4 : {"min": 664, "max": 667},
        7.5 : {"min": 668, "max": 669},
        7.6 : {"min": 670, "max": 671},
        7.7 : {"min": 672, "max": 674},
        7.8 : {"min": 675, "max": 676},
        7.9 : {"min": 677, "max": 679},
        8 : {"min": 680, "max": 681},
        8.1 : {"min": 682, "max": 683},
        8.2 : {"min": 684, "max": 686},
        8.3 : {"min": 687, "max": 689},
        8.4 : {"min": 690, "max": 693},
        8.5 : {"min": 694, "max": 696},
        8.6 : {"min": 697, "max": 700},
        8.7 : {"min": 701, "max": 704},
        8.8 : {"min": 705, "max": 708},
        8.9 : {"min": 709, "max": 713},
        9 : {"min": 714, "max": 720},
        9.1 : {"min": 721, "max": 727},
        9.2 : {"min": 728, "max": 734},
        9.3 : {"min": 735, "max": 742},
        9.4 : {"min": 743, "max": 749},
        9.5 : {"min": 750, "max": 756},
        9.6 : {"min": 757, "max": 762},
        9.7 : {"min": 763, "max": 769},
        9.8 : {"min": 770, "max": 776},
        9.9 : {"min": 777, "max": 783},
        10 : {"min": 784, "max": 784},
        10.1 : {"min": 785, "max": 787},
        10.2 : {"min": 788, "max": 790},
        10.3 : {"min": 791, "max": 794},
        10.4 : {"min": 795, "max": 798},
        10.5 : {"min": 799, "max": 808},
        10.6 : {"min": 809, "max": 819},
        10.7 : {"min": 820, "max": 830},
        10.8 : {"min": 831, "max": 843},
        10.9 : {"min": 844, "max": 855},
        11 : {"min": 856, "max": 866},
        11.1 : {"min": 867, "max": 875},
        11.2 : {"min": 876, "max": 885},
        11.3 : {"min": 886, "max": 893},
        11.4 : {"min": 894, "max": 901},
        11.5 : {"min": 902, "max": 907},
        11.6 : {"min": 908, "max": 913},
        11.7 : {"min": 914, "max": 918},
        11.8 : {"min": 919, "max": 922},
        11.9 : {"min": 923, "max": 926},
        12 : {"min": 927, "max": 927},
        12.3 : {"min": 928, "max": 929},
        12.6 : {"min": 930, "max": 931},
        12.7 : {"min": 932, "max": 934},
        12.8 : {"min": 935, "max": 937},
        12.9 : {"min": 938, "max": 940},
        13 : {"min": 941, "max": 943},
        13.1 : {"min": 944, "max": 947},
        13.2 : {"min": 948, "max": 950},
        13.3 : {"min": 951, "max": 953},
        13.4 : {"min": 954, "max": 957},
        13.5 : {"min": 958, "max": 960},
        13.6 : {"min": 961, "max": 964},
        13.7 : {"min": 965, "max": 967},
        13.8 : {"min": 968, "max": 970},
        13.9 : {"min": 971, "max": 973},
        14 : {"min": 974, "max": 976},
        14.1 : {"min": 977, "max": 978},
        14.2 : {"min": 979, "max": 980},
        14.3 : {"min": 981, "max": 982},
        14.4 : {"min": 983, "max": 984},
        14.5 : {"min": 985, "max": 986},
        14.6 : {"min": 987, "max": 987},
        14.7 : {"min": 988, "max": 989},
        14.8 : {"min": 990, "max": 990},
        15 : {"min": 991, "max": 991},
        15.2 : {"min": 992, "max": 992},
        15.4 : {"min": 993, "max": 993},
        15.7 : {"min": 994, "max": 994},
        15.9 : {"min": 995, "max": 995},
        16.3 : {"min": 996, "max": 996},
        17.2 : {"min": 997, "max": 999},
        17.3 : {"min": 999, "max": 1000}
    },
};

var level_to_grade = {
    'male' : {
        'radius' : {
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
        'capitate' : {
            0 : 0,
            1 : 8,
            2 : 18,
            3 : 37,
            4 : 58,
            5 : 75,
            6 : 89,
            7 : 129,
        },
        'hamate' : {
            0 : 0,
            1 : 11,
            2 : 25,
            3 : 53,
            4 : 73,
            5 : 87,
            6 : 99,
            7 : 109,
            8 : 135,
        },
        'first-metacarpal' : {
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
        'third-metacarpal' : {
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
        'fifth-metacarpal' : {
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
        'first-proximal-phalange' : {
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
        'third-proximal-phalange' : {
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
        'fifth-proximal-phalange' : {
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
        'third-middle-phalange' : {
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
        'fifth-middle-phalange' : {
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
        'first-distal-phalange' : {
            0 : 0,
            1 : 18,
            2 : 23,
            3 : 47,
            4 : 62,
            5 : 73,
            6 : 91,
            7 : 95,
            8 : 102,
        },
        'third-distal-phalange' : {
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
        'fifth-distal-phalange' : {
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
    'female' : {
        'radius' : {
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
        'capitate' : {
            0 : 0,
            1 : 3,
            2 : 14,
            3 : 39,
            4 : 53,
            5 : 63,
            6 : 72,
            7 : 100,
        },
        'hamate' : {
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
        'first-metacarpal' : {
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
        'third-metacarpal' : {
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
        'fifth-metacarpal' : {
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
        'first-proximal-phalange' : {
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
        'third-proximal-phalange' : {
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
        'fifth-proximal-phalange' : {
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
        'third-middle-phalange' : {
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
        'fifth-middle-phalange' : {
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
        'first-distal-phalange' : {
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
        'third-distal-phalange' : {
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
        'fifth-distal-phalange' : {
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
};

/* RUS全局方法 */

//切换骨骼时对骨骼详情部分（评分评级、备注、骨龄）的页面变化
$.fn.switch_bone = function(bone_name_key){
    $("div[class=cropper-canvas] img").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    $.fn.update_bone_age()
    var bone = bones[bone_name_key]
    if(bone['error'] == 0){
        $("#bone_discription").attr('hidden','hidden')
        $("#form_bone_details").removeAttr('hidden')
        $("#modify_bone_position").attr('hidden','hidden')
        $("#modify_bone_detail").attr('hidden','hidden')
        $('small[id^=bone_discription_text]').attr('hidden','hidden')
        $("#bone_details_name").text(bone['name'])
        $("#bone_details_remarks").val(bone['remarks'])
        if(bone['level'] > 0){
            $("#bone_discription").removeAttr("hidden", "hidden");
            $("#bone_discription_img").attr("src", url_static + "BoneAge/img/CHN/" + bone_name_key + "-" + bone['level'] + ".png")
            $("#bone_discription_text_" + bone_name_key + "_" + bone['level']).removeAttr('hidden', 'hidden')
        }
        switch (bone_name_key) {
            case 'radius' : $("#bone_details_level").attr('max','10'); break;
            case 'capitate' : $("#bone_details_level").attr('max','7'); break;
            case 'hamate' : $("#bone_details_level").attr('max','8'); break;
            case 'first-metacarpal' : $("#bone_details_level").attr('max','8'); break;
            case 'third-metacarpal' : $("#bone_details_level").attr('max','8'); break;
            case 'fifth-metacarpal' : $("#bone_details_level").attr('max','8'); break;
            case 'first-proximal-phalange' : $("#bone_details_level").attr('max','8'); break;
            case 'third-proximal-phalange' : $("#bone_details_level").attr('max','8'); break;
            case 'fifth-proximal-phalange' : $("#bone_details_level").attr('max','8'); break;
            case 'third-middle-phalange' : $("#bone_details_level").attr('max','8'); break;
            case 'fifth-middle-phalange' : $("#bone_details_level").attr('max','8'); break;
            case 'first-distal-phalange' : $("#bone_details_level").attr('max','8'); break;
            case 'third-distal-phalange' : $("#bone_details_level").attr('max','8'); break;
            case 'fifth-distal-phalange' : $("#bone_details_level").attr('max','8'); break;
            default:
                alert('致命错误：json中未找到该骨骼');
        }
        if(bone['level'] >= 0){
            $("#bone_details_level_label").text(bone['level'])
            $("#level-" + bone_name_key).text(bone['level'] + ' 级')
            $("#bone_details_level").val(bone['level'])
        }
        else{
            $("#bone_details_level_label").text("？")
            $("#bone_details_level").val(0)
        }
    }
    else{
        $("#bone_details_name").text(bone['name'] + "（" + bone['error_message'] + "）")
        $("#form_bone_details").attr('hidden','hidden')
    }
    $("#bone_details_level").focus()
};
/* 如果所有骨骼等级数据与定位正常，则计算分数并显示参考年龄 */
$.fn.update_bone_age = function(){
    $('#warning_age_misregistration').attr('hidden', 'hidden');
    $('#bone_age_great_differ_warning').hide();
    $("#bone_age").removeAttr('disabled');
    $("#bone_age").attr('placeholder','')
    $('#label_bone_age').removeClass('text-danger');
    $("#label_bone_age").text('');
    var is_valid = true
    $.each(bones, function(bone_name_key, bone_details){
        if(bone_details['level'] < 0) is_valid = false
        if(bone_details['error'] != 0) is_valid = false
    })
    if(is_valid){
        grade = 0
        bone_age = -1
        
        $.each(bones, function(bone_name_key,bone_details){
            grade += level_to_grade[sex][bone_name_key][bone_details['level']]
        })
        // CHN分数转年龄
        $.each(grade_to_age[sex], function(age,range){
            if(grade >= range['min'] && grade <= range['max']){
                bone_age = age
            }
        })

        // 前端骨龄修改
        if(bone_age >= 0){
            $("#bone_age").val(bone_age);
            $("#label_bone_age").text(bone_age + "岁");
            $("#label_bone_grade").text(grade + "分");
            // 差距过大提示
            if(Math.abs(actual_age - bone_age) >= 1){
                $("#warning_age_misregistration").removeAttr('hidden');
                $("#bone_age_great_differ_warning").show()
            }
        }
    }
    else{
        $("#bone_age").attr('disabled', 'disabled');
        $("#bone_age").attr('placeholder', '*无法计算，骨骼数据存在错误*');
        $("#label_bone_age").addClass('text-danger');
        $("#label_bone_age").text('*无法计算*');
    }
};

/* CHN页面初始化 */
$(document).ready(function () {
    /*popover提示框全局覆盖*/
    var tooltipTriggerList = Array.prototype.slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    $.fn.switch_bone(default_bone)
    /* 焦点至评级条 */
    $("#bone_details_level").focus()

    /* 如果数据库中存在骨龄数据，则用数据库中的值 */
    if(task['bone_age'] >= 0){
        $("#bone_age").val(task['bone_age']);
        $("#label_bone_age").text(task['bone_age'] + "岁");
    }
});

/* 评分评级修改后弹出保存按钮 */
$("#bone_details_level").on('input', function (e) { 
    var bone_name_key = $(".list-group-item-action.active>span[id^=view-]").attr('id').substring(5)
    var bone = bones[bone_name_key]
    level = bone['level']
    $("#level-fifth-metacarpal").removeClass('text-danger')
    $("#bone_details_level_label").text($(this).val())
    $("#level-" + bone_name_key).text(bone['level'] + " 级")
    $("#modify_bone_detail").removeAttr('hidden')
    if($(this).val() >= 0){
        $("#bone_discription").removeAttr("hidden", "hidden");
        $("small[id^=bone_discription_text_]").attr('hidden', 'hidden')
        $("#bone_discription_text_" + bone_name_key + "_" + $(this).val()).removeAttr('hidden', 'hidden')
        $("#bone_discription_img").attr("src", url_static + "BoneAge/img/CHN/" + bone_name_key + "-" + $(this).val() + ".png")
    }
    else{
        $("#bone_discription").attr('hidden','hidden')
    }
    
    bone['level'] = $("#bone_details_level").val()
    $.fn.update_bone_age()
    bone['level'] = level
});