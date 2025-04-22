from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p3_decision_tree(R, G, B):
    if G <= 1.0:
        return None
    else:  # if G > 1.0
        if R <= 12.5:
            if B <= 0.5:
                return Color.BLACK
            else:  # if B > 0.5
                if G <= 8.5:
                    return Color.BROWN
                else:  # if G > 8.5
                    if R <= 5.5:
                        return Color.GREEN
                    else:  # if R > 5.5
                        return Color.BLUE
        else:  # if R > 12.5
            if B <= 3.0:
                return Color.RED
            else:  # if B > 3.0
                if B <= 14.5:
                    return Color.YELLOW
                else:  # if B > 14.5
                    return Color.WHITE
