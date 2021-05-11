#!/usr/bin/env python
#======================================================================================================================

def getInput(MAX, deep = "N"):

    while True:
        
        try:
            if deep == "Y":
                rowSelect = input("Select a row [Type DEEP for searching other databases]: ")
            else:
                rowSelect = input("Select a row: ")

            # Exit code.
            if rowSelect in ["exit", "quit"]:
                return 999

            # Deep search code.
            if rowSelect.upper() in ["DEEP", "D"] and deep == "Y":
                print("")
                return 404

            # Validating input
            rowSelect = int(rowSelect)
            if rowSelect > MAX or rowSelect == 0:
                print("Error: Please input a valid row number.")
                continue
            break

        except:
            print("Error: Please input a valid row number.")
            continue

    print("")

    return rowSelect

#======================================================================================================================