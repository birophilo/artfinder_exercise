TEST_FIXTURES_BASIC = [
    {
        # standard test case, test several results, different percentages
        "input": "France Italy Germany",
        "expected": [
            "file_02.txt: 100%",
            "file_04.txt: 67%",
            "file_03.txt: 67%",
            "file_05.txt: 33%"
        ]
    },
    {
        # check input handling is case insensitive
        "input": "france italy Germany",
        "expected": [
            "file_02.txt: 100%",
            "file_04.txt: 67%",
            "file_03.txt: 67%",
            "file_05.txt: 33%"
        ]
    },
    {
        # check results are limited to 10 files
        "input": "the",
        "expected": [
            "file_12.txt: 100%",
            "file_06.txt: 100%",
            "file_07.txt: 100%",
            "file_13.txt: 100%",
            "file_05.txt: 100%",
            "file_11.txt: 100%",
            "file_10.txt: 100%",
            "file_04.txt: 100%",
            "file_14.txt: 100%",
            "file_01.txt: 100%"
        ]
    }
]

TEST_FIXTURES_ADVANCED = [
    {
        # score: total occurrences of matching words * percentage matching
        "input": "France Italy Germany",
        "expected": [
            "file_02.txt: 11.00",  # france article
            "file_03.txt: 8.00",  # germany article
            "file_04.txt: 6.00",  # italy article
            "file_05.txt: 0.33"  # spain article
        ]
    }
]
