import pandas as pd


def get_camps():
    data = [
        {
            "Camp": "Camp 1",
            "People": 350,
            "Health Risk": 60,
            "Vulnerable": 40,
            "Time Without Aid": 20,
            "Isolation": 30,
            "Water Need": 1200,
            "Food Need": 500,
            "Medical Need": 15,
        },
        {
            "Camp": "Camp 2",
            "People": 520,
            "Health Risk": 90,
            "Vulnerable": 80,
            "Time Without Aid": 24,
            "Isolation": 85,
            "Water Need": 2200,
            "Food Need": 800,
            "Medical Need": 35,
        },
        {
            "Camp": "Camp 3",
            "People": 280,
            "Health Risk": 50,
            "Vulnerable": 55,
            "Time Without Aid": 10,
            "Isolation": 25,
            "Water Need": 900,
            "Food Need": 400,
            "Medical Need": 10,
        },
        {
            "Camp": "Camp 4",
            "People": 610,
            "Health Risk": 85,
            "Vulnerable": 90,
            "Time Without Aid": 23,
            "Isolation": 90,
            "Water Need": 2800,
            "Food Need": 1000,
            "Medical Need": 40,
        },
        {
            "Camp": "Camp 5",
            "People": 430,
            "Health Risk": 70,
            "Vulnerable": 65,
            "Time Without Aid": 16,
            "Isolation": 60,
            "Water Need": 1700,
            "Food Need": 650,
            "Medical Need": 20,
        },
    ]

    return pd.DataFrame(data)


def get_warehouses():
    data = [
        {
            "Warehouse": "Warehouse A",
            "Water": 5000,
            "Food": 2000,
            "Medical": 100,
        },
        {
            "Warehouse": "Warehouse B",
            "Water": 3500,
            "Food": 3000,
            "Medical": 120,
        },
        {
            "Warehouse": "Warehouse C",
            "Water": 4500,
            "Food": 2500,
            "Medical": 150,
        },
        {
            "Warehouse": "Warehouse D",
            "Water": 3000,
            "Food": 1800,
            "Medical": 80,
        },
    ]

    return pd.DataFrame(data)
