from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p4_decision_tree(R, G, B):
    if R <= 1.0:
        return None
    else:  # if R > 1.0
        if B <= 21.5:
            if G <= 22.0:
                if B <= 7.0:
                    if R <= 20.5:
                        if G <= 7.5:
                            if R <= 4.5:
                                return Color.BLACK
                            else:  # if R > 4.5
                                return Color.BROWN
                        else:  # if G > 7.5
                            return Color.GREEN
                    else:  # if R > 20.5
                        return Color.RED
                else:  # if B > 7.0
                    return Color.BLUE
            else:  # if G > 22.0
                return Color.YELLOW
        else:  # if B > 21.5
            return Color.WHITE
