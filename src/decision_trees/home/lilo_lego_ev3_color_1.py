from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p1_decision_tree(R, G, B):
    if G <= 3.5:
        return None
    else:  # if G > 3.5
        if G <= 25.0:
            if R <= 23.0:
                if B <= 11.5:
                    if G <= 13.5:
                        if R <= 5.5:
                            return Color.BLACK
                        else:  # if R > 5.5
                            return Color.BROWN
                    else:  # if G > 13.5
                        return Color.GREEN
                else:  # if B > 11.5
                    return Color.BLUE
            else:  # if R > 23.0
                return Color.RED
        else:  # if G > 25.0
            if B <= 27.5:
                return Color.YELLOW
            else:  # if B > 27.5
                return Color.WHITE
