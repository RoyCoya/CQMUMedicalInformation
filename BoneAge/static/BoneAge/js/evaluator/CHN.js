/* CHN等级、分数、年龄转换表 */
var grade_to_age = {
    'male' : {
        0.0 : {min : 0.0, max : 4.0},
        0.1 : {min : 5.0, max : 14.0},
        0.2 : {min : 15.0, max : 23.0},
        0.3 : {min : 24.0, max : 30.0},
        0.4 : {min : 31.0, max : 37.0},
        0.5 : {min : 38.0, max : 43.0},
        0.6 : {min : 44.0, max : 45.0},
        0.7 : {min : 46.0, max : 47.0},
        0.8 : {min : 48.0, max : 51.0},
        0.9 : {min : 52.0, max : 55.0},
        1.0 : {min : 56.0, max : 61.0},
        1.1 : {min : 62.0, max : 76.0},
        1.2 : {min : 77.0, max : 93.0},
        1.3 : {min : 94.0, max : 111.0},
        1.4 : {min : 112.0, max : 131.0},
        1.5 : {min : 132.0, max : 152.0},
        1.6 : {min : 153.0, max : 169.0},
        1.7 : {min : 170.0, max : 186.0},
        1.8 : {min : 187.0, max : 203.0},
        1.9 : {min : 204.0, max : 220.0},
        2.0 : {min : 221.0, max : 236.0},
        2.1 : {min : 237.0, max : 252.0},
        2.2 : {min : 253.0, max : 270.0},
        2.3 : {min : 271.0, max : 287.0},
        2.4 : {min : 288.0, max : 303.0},
        2.5 : {min : 304.0, max : 319.0},
        2.6 : {min : 320.0, max : 333.0},
        2.7 : {min : 334.0, max : 346.0},
        2.8 : {min : 347.0, max : 358.0},
        2.9 : {min : 359.0, max : 370.0},
        3.0 : {min : 371.0, max : 380.0},
        3.1 : {min : 381.0, max : 390.0},
        3.2 : {min : 391.0, max : 399.0},
        3.3 : {min : 400.0, max : 407.0},
        3.4 : {min : 408.0, max : 415.0},
        3.5 : {min : 416.0, max : 422.0},
        3.6 : {min : 423.0, max : 429.0},
        3.7 : {min : 430.0, max : 436.0},
        3.8 : {min : 437.0, max : 442.0},
        3.9 : {min : 443.0, max : 448.0},
        4.0 : {min : 449.0, max : 453.0},
        4.1 : {min : 454.0, max : 457.0},
        4.2 : {min : 458.0, max : 461.0},
        4.3 : {min : 462.0, max : 465.0},
        4.4 : {min : 466.0, max : 468.0},
        4.5 : {min : 469.0, max : 472.0},
        4.6 : {min : 473.0, max : 476.0},
        4.7 : {min : 477.0, max : 481.0},
        4.8 : {min : 482.0, max : 485.0},
        4.9 : {min : 486.0, max : 490.0},
        5.0 : {min : 491.0, max : 495.0},
        5.1 : {min : 496.0, max : 498.0},
        5.2 : {min : 499.0, max : 502.0},
        5.3 : {min : 503.0, max : 506.0},
        5.4 : {min : 507.0, max : 510.0},
        5.5 : {min : 511.0, max : 511.0},
        5.6 : {min : 512.0, max : 518.0},
        5.7 : {min : 519.0, max : 521.0},
        5.8 : {min : 522.0, max : 525.0},
        5.9 : {min : 526.0, max : 529.0},
        6.0 : {min : 530.0, max : 532.0},
        6.1 : {min : 533.0, max : 536.0},
        6.2 : {min : 537.0, max : 540.0},
        6.3 : {min : 541.0, max : 544.0},
        6.4 : {min : 545.0, max : 548.0},
        6.5 : {min : 549.0, max : 552.0},
        6.6 : {min : 553.0, max : 556.0},
        6.7 : {min : 557.0, max : 560.0},
        6.8 : {min : 561.0, max : 564.0},
        6.9 : {min : 565.0, max : 567.0},
        7.0 : {min : 568.0, max : 571.0},
        7.1 : {min : 572.0, max : 574.0},
        7.2 : {min : 575.0, max : 577.0},
        7.3 : {min : 578.0, max : 580.0},
        7.4 : {min : 581.0, max : 583.0},
        7.5 : {min : 584.0, max : 586.0},
        7.6 : {min : 587.0, max : 589.0},
        7.7 : {min : 590.0, max : 591.0},
        7.8 : {min : 592.0, max : 594.0},
        7.9 : {min : 595.0, max : 597.0},
        8.0 : {min : 598.0, max : 599.0},
        8.1 : {min : 600.0, max : 603.0},
        8.2 : {min : 604.0, max : 606.0},
        8.3 : {min : 607.0, max : 610.0},
        8.4 : {min : 611.0, max : 613.0},
        8.5 : {min : 614.0, max : 616.0},
        8.6 : {min : 617.0, max : 619.0},
        8.7 : {min : 620.0, max : 622.0},
        8.8 : {min : 623.0, max : 625.0},
        8.9 : {min : 626.0, max : 628.0},
        9.0 : {min : 629.0, max : 631.0},
        9.1 : {min : 632.0, max : 633.0},
        9.2 : {min : 634.0, max : 635.0},
        9.3 : {min : 636.0, max : 637.0},
        9.4 : {min : 638.0, max : 638.0},
        9.5 : {min : 639.0, max : 640.0},
        9.6 : {min : 641.0, max : 642.0},
        9.7 : {min : 643.0, max : 644.0},
        9.8 : {min : 645.0, max : 646.0},
        9.9 : {min : 647.0, max : 648.0},
        10.0 : {min : 649.0, max : 650.0},
        10.1 : {min : 651.0, max : 654.0},
        10.2 : {min : 655.0, max : 657.0},
        10.3 : {min : 658.0, max : 661.0},
        10.4 : {min : 662.0, max : 665.0},
        10.5 : {min : 666.0, max : 669.0},
        10.6 : {min : 670.0, max : 673.0},
        10.7 : {min : 674.0, max : 677.0},
        10.8 : {min : 678.0, max : 682.0},
        10.9 : {min : 683.0, max : 685.0},
        11.0 : {min : 686.0, max : 691.0},
        11.1 : {min : 692.0, max : 694.0},
        11.2 : {min : 695.0, max : 698.0},
        11.3 : {min : 699.0, max : 702.0},
        11.4 : {min : 703.0, max : 706.0},
        11.5 : {min : 707.0, max : 711.0},
        11.6 : {min : 712.0, max : 716.0},
        11.7 : {min : 717.0, max : 731.0},
        11.8 : {min : 732.0, max : 726.0},
        11.9 : {min : 727.0, max : 732.0},
        12.0 : {min : 733.0, max : 738.0},
        12.1 : {min : 739.0, max : 745.0},
        12.2 : {min : 746.0, max : 753.0},
        12.3 : {min : 754.0, max : 761.0},
        12.4 : {min : 762.0, max : 770.0},
        12.5 : {min : 771.0, max : 779.0},
        12.6 : {min : 780.0, max : 788.0},
        12.7 : {min : 789.0, max : 798.0},
        12.8 : {min : 799.0, max : 808.0},
        12.9 : {min : 809.0, max : 818.0},
        13.0 : {min : 819.0, max : 828.0},
        13.1 : {min : 829.0, max : 840.0},
        13.2 : {min : 841.0, max : 851.0},
        13.3 : {min : 852.0, max : 862.0},
        13.4 : {min : 863.0, max : 873.0},
        13.5 : {min : 874.0, max : 883.0},
        13.6 : {min : 884.0, max : 892.0},
        13.7 : {min : 893.0, max : 901.0},
        13.8 : {min : 902.0, max : 906.0},
        13.9 : {min : 907.0, max : 914.0},
        14.0 : {min : 915.0, max : 915.0},
        14.1 : {min : 916.0, max : 921.0},
        14.2 : {min : 922.0, max : 922.0},
        14.3 : {min : 923.0, max : 923.0},
        14.6 : {min : 924.0, max : 924.0},
        14.7 : {min : 925.0, max : 925.0},
        14.8 : {min : 926.0, max : 927.0},
        14.9 : {min : 928.0, max : 929.0},
        15.0 : {min : 930.0, max : 931.0},
        15.1 : {min : 932.0, max : 936.0},
        15.2 : {min : 937.0, max : 940.0},
        15.3 : {min : 941.0, max : 945.0},
        15.4 : {min : 946.0, max : 950.0},
        15.5 : {min : 951.0, max : 955.0},
        15.6 : {min : 956.0, max : 960.0},
        15.7 : {min : 961.0, max : 964.0},
        15.8 : {min : 965.0, max : 969.0},
        15.9 : {min : 970.0, max : 974.0},
        16.0 : {min : 975.0, max : 979.0},
        16.1 : {min : 980.0, max : 982.0},
        16.2 : {min : 983.0, max : 985.0},
        16.3 : {min : 986.0, max : 987.0},
        16.4 : {min : 988.0, max : 989.0},
        16.5 : {min : 990.0, max : 990.0},
        16.8 : {min : 991.0, max : 991.0},
        17.0 : {min : 992.0, max : 992.0},
        17.6 : {min : 993.0, max : 993.0},
        18.4 : {min : 994.0, max : 1000},
    },
    'female' : {
        0.0 : {min : 0.0, max : 2.0},
        0.1 : {min : 3.0, max : 5.0},
        0.2 : {min : 6.0, max : 11.0},
        0.3 : {min : 12.0, max : 17.0},
        0.4 : {min : 18.0, max : 25.0},
        0.5 : {min : 26.0, max : 34.0},
        0.6 : {min : 35.0, max : 40.0},
        0.7 : {min : 41.0, max : 50.0},
        0.8 : {min : 51.0, max : 63.0},
        0.9 : {min : 64.0, max : 81.0},
        1.0 : {min : 82.0, max : 102.0},
        1.1 : {min : 103.0, max : 145.0},
        1.2 : {min : 146.0, max : 189.0},
        1.3 : {min : 190.0, max : 235.0},
        1.4 : {min : 236.0, max : 281.0},
        1.5 : {min : 282.0, max : 329.0},
        1.6 : {min : 330.0, max : 361.0},
        1.7 : {min : 362.0, max : 390.0},
        1.8 : {min : 391.0, max : 415.0},
        1.9 : {min : 416.0, max : 437.0},
        2.0 : {min : 438.0, max : 455.0},
        2.1 : {min : 456.0, max : 470.0},
        2.2 : {min : 471.0, max : 482.0},
        2.3 : {min : 483.0, max : 492.0},
        2.4 : {min : 493.0, max : 500.0},
        2.5 : {min : 501.0, max : 505.0},
        2.6 : {min : 506.0, max : 511.0},
        2.7 : {min : 512.0, max : 516.0},
        2.8 : {min : 517.0, max : 521.0},
        2.9 : {min : 522.0, max : 527.0},
        3.0 : {min : 528.0, max : 532.0},
        3.1 : {min : 533.0, max : 535.0},
        3.2 : {min : 536.0, max : 539.0},
        3.3 : {min : 540.0, max : 542.0},
        3.4 : {min : 543.0, max : 544.0},
        3.5 : {min : 545.0, max : 547.0},
        3.6 : {min : 548.0, max : 549.0},
        3.7 : {min : 550.0, max : 552.0},
        3.8 : {min : 553.0, max : 554.0},
        3.9 : {min : 555.0, max : 556.0},
        4.0 : {min : 557.0, max : 558.0},
        4.1 : {min : 559.0, max : 562.0},
        4.2 : {min : 563.0, max : 566.0},
        4.3 : {min : 567.0, max : 571.0},
        4.4 : {min : 572.0, max : 575.0},
        4.5 : {min : 576.0, max : 580.0},
        4.6 : {min : 581.0, max : 583.0},
        4.7 : {min : 584.0, max : 585.0},
        4.8 : {min : 586.0, max : 588.0},
        4.9 : {min : 589.0, max : 591.0},
        5.0 : {min : 592.0, max : 594.0},
        5.1 : {min : 595.0, max : 597.0},
        5.2 : {min : 598.0, max : 601.0},
        5.3 : {min : 602.0, max : 605.0},
        5.4 : {min : 606.0, max : 608.0},
        5.5 : {min : 609.0, max : 612.0},
        5.6 : {min : 613.0, max : 616.0},
        5.7 : {min : 617.0, max : 620.0},
        5.8 : {min : 621.0, max : 623.0},
        5.9 : {min : 624.0, max : 627.0},
        6.0 : {min : 628.0, max : 631.0},
        6.1 : {min : 632.0, max : 634.0},
        6.2 : {min : 635.0, max : 637.0},
        6.3 : {min : 638.0, max : 640.0},
        6.4 : {min : 641.0, max : 642.0},
        6.5 : {min : 643.0, max : 645.0},
        6.6 : {min : 646.0, max : 647.0},
        6.7 : {min : 648.0, max : 650.0},
        6.8 : {min : 651.0, max : 652.0},
        6.9 : {min : 653.0, max : 654.0},
        7.0 : {min : 655.0, max : 657.0},
        7.1 : {min : 658.0, max : 659.0},
        7.2 : {min : 660.0, max : 661.0},
        7.3 : {min : 662.0, max : 663.0},
        7.4 : {min : 664.0, max : 665.0},
        7.5 : {min : 666.0, max : 668.0},
        7.6 : {min : 669.0, max : 670.0},
        7.7 : {min : 671.0, max : 672.0},
        7.8 : {min : 673.0, max : 675.0},
        7.9 : {min : 676.0, max : 677.0},
        8.0 : {min : 678.0, max : 680.0},
        8.1 : {min : 681.0, max : 682.0},
        8.2 : {min : 683.0, max : 684.0},
        8.3 : {min : 685.0, max : 687.0},
        8.4 : {min : 688.0, max : 690.0},
        8.5 : {min : 691.0, max : 694.0},
        8.6 : {min : 695.0, max : 697.0},
        8.7 : {min : 698.0, max : 701.0},
        8.8 : {min : 702.0, max : 705.0},
        8.9 : {min : 706.0, max : 709.0},
        9.0 : {min : 710.0, max : 714.0},
        9.1 : {min : 715.0, max : 721.0},
        9.2 : {min : 722.0, max : 728.0},
        9.3 : {min : 729.0, max : 735.0},
        9.4 : {min : 736.0, max : 743.0},
        9.5 : {min : 744.0, max : 750.0},
        9.6 : {min : 751.0, max : 757.0},
        9.7 : {min : 758.0, max : 763.0},
        9.8 : {min : 764.0, max : 770.0},
        9.9 : {min : 771.0, max : 777.0},
        10.0 : {min : 778.0, max : 784.0},
        10.1 : {min : 785.0, max : 785.0},
        10.2 : {min : 786.0, max : 788.0},
        10.3 : {min : 789.0, max : 791.0},
        10.4 : {min : 792.0, max : 795.0},
        10.5 : {min : 796.0, max : 799.0},
        10.6 : {min : 800.0, max : 809.0},
        10.7 : {min : 810.0, max : 820.0},
        10.8 : {min : 821.0, max : 831.0},
        10.9 : {min : 832.0, max : 844.0},
        11.0 : {min : 845.0, max : 856.0},
        11.1 : {min : 857.0, max : 867.0},
        11.2 : {min : 868.0, max : 876.0},
        11.3 : {min : 877.0, max : 886.0},
        11.4 : {min : 887.0, max : 894.0},
        11.5 : {min : 895.0, max : 902.0},
        11.6 : {min : 903.0, max : 908.0},
        11.7 : {min : 909.0, max : 914.0},
        11.8 : {min : 915.0, max : 919.0},
        11.9 : {min : 920.0, max : 923.0},
        12.0 : {min : 924.0, max : 927.0},
        12.2 : {min : 928.0, max : 928.0},
        12.6 : {min : 929.0, max : 930.0},
        12.7 : {min : 931.0, max : 932.0},
        12.8 : {min : 933.0, max : 935.0},
        12.9 : {min : 936.0, max : 938.0},
        13.0 : {min : 939.0, max : 941.0},
        13.1 : {min : 942.0, max : 944.0},
        13.2 : {min : 945.0, max : 948.0},
        13.3 : {min : 949.0, max : 951.0},
        13.4 : {min : 952.0, max : 954.0},
        13.5 : {min : 955.0, max : 958.0},
        13.6 : {min : 959.0, max : 961.0},
        13.7 : {min : 962.0, max : 965.0},
        13.8 : {min : 966.0, max : 968.0},
        13.9 : {min : 969.0, max : 971.0},
        14.0 : {min : 972.0, max : 974.0},
        14.1 : {min : 975.0, max : 977.0},
        14.2 : {min : 978.0, max : 979.0},
        14.3 : {min : 980.0, max : 981.0},
        14.4 : {min : 982.0, max : 983.0},
        14.5 : {min : 984.0, max : 985.0},
        14.6 : {min : 986.0, max : 987.0},
        14.7 : {min : 988.0, max : 988.0},
        14.8 : {min : 989.0, max : 990.0},
        14.9 : {min : 991.0, max : 991.0},
        15.2 : {min : 992.0, max : 992.0},
        15.4 : {min : 993.0, max : 993.0},
        15.7 : {min : 994.0, max : 994.0},
        15.9 : {min : 995.0, max : 995.0},
        16.3 : {min : 996.0, max : 996.0},
        17.2 : {min : 997.0, max : 997.0},
        17.3 : {min : 998.0, max : 1000.0},
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
            6 : 80,
            7 : 129,
        },
        'hamate' : {
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
            4 : 52,
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