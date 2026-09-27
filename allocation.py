def allocate_supplies(camps, warehouses):

    camps = camps.sort_values(
        by="Priority Score",
        ascending=False
    ).copy()

    warehouses = warehouses.copy()

    allocations = []

    for _, camp in camps.iterrows():

        remaining_water = camp["Water Need"]
        remaining_food = camp["Food Need"]
        remaining_medical = camp["Medical Need"]

        for index, warehouse in warehouses.iterrows():

            if (
                remaining_water <= 0
                and remaining_food <= 0
                and remaining_medical <= 0
            ):
                break

            water = min(
                remaining_water,
                warehouses.loc[index, "Water"]
            )

            food = min(
                remaining_food,
                warehouses.loc[index, "Food"]
            )

            medical = min(
                remaining_medical,
                warehouses.loc[index, "Medical"]
            )

            if water > 0 or food > 0 or medical > 0:

                allocations.append({
                    "Camp": camp["Camp"],
                    "Warehouse": warehouse["Warehouse"],
                    "Water": water,
                    "Food": food,
                    "Medical": medical,
                    "Priority Score": camp["Priority Score"]
                })

                warehouses.loc[index, "Water"] -= water
                warehouses.loc[index, "Food"] -= food
                warehouses.loc[index, "Medical"] -= medical

                remaining_water -= water
                remaining_food -= food
                remaining_medical -= medical

    return allocations, warehouses
