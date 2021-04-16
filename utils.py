import buttonHandler as bh

def get_button_from_hand(hand_coords):
    #input - 21 hand coord, output - buttons list with desired properties
    buttons = []
    hand_type = get_hand_type(hand_coords)
    if hand_type == "fist":
        button = bh.ButtonHandler.getInstance().get_new_button("fist_hand")
        button.set_coords(hand_coords[12][1], hand_coords[12][2])
        button.set_button_type("fist")
        buttons.append(button)
    elif "palm":
        button = bh.ButtonHandler.getInstance().get_new_button("palm_index_f")
        button.set_coords(hand_coords[8][1], hand_coords[8][2])
        button.set_button_type("palm")
        buttons.append(button)
        button = bh.ButtonHandler.getInstance().get_new_button("palm_ring_f")
        button.set_coords(hand_coords[16][1], hand_coords[16][2])
        button.set_button_type("palm")
        buttons.append(button)


    return buttons


def get_hand_type(hand):

    if hand[0][1] > hand[8][1] > hand[6][1] or hand[0][1] < hand[8][1] < hand[6][1] \
            and hand[0][1] > hand[12][1] > hand[10][1] or hand[0][1] < hand[12][1] < hand[10][1] \
            and hand[0][1] < hand[16][1] < hand[14][1] or hand[0][1] < hand[16][1] < hand[14][1]:
        return "fist"
    elif (hand[6][1] > hand[7][1] > hand[8][1] or hand[6][1] < hand[7][1] < hand[8][1] \
          or hand[6][2] > hand[7][2] > hand[8][1] or hand[6][2] < hand[7][2] < hand[8][2]) and (
            hand[10][1] > hand[11][1] > hand[12][1] or hand[10][1] < hand[11][1] < hand[12][1] \
            or hand[10][2] > hand[11][2] > hand[12][2] or hand[10][2] < hand[11][2] < hand[12][2]) and (
            hand[14][1] > hand[15][1] > hand[16][1] or hand[14][1] < hand[15][1] < hand[16][1] \
            or hand[14][2] > hand[15][2] > hand[16][2] or hand[14][2] < hand[15][2] < hand[16][2]):
        return "palm"
    else:
        return "unknown"
