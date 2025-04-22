from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p2_decision_tree(R, G, B):
    if R <= 11.0:
        if B <= 4.5:
            if R <= 1.0:
                return None
            else:  # if R > 1.0
                if G <= 9.5:
                    if G <= 5.5:
                        return Color.BROWN
                    else:  # if G > 5.5
                        return Color.BLACK
                else:  # if G > 9.5
                    return Color.GREEN
        else:  # if B > 4.5
            return Color.BLUE
    else:  # if R > 11.0
        if G <= 14.0:
            return Color.RED
        else:  # if G > 14.0
            if B <= 11.0:
                return Color.YELLOW
            else:  # if B > 11.0
                return Color.WHITE
