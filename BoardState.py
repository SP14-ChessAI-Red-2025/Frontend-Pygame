class BoardState():
    def __init__(self):
        #creates 2d array of starting board state
        self.game_board = [
            ["blk_rook", "blk_knight", "blk_bishop", "blk_queen", "blk_king", "blk_bishop", "blk_knight", "blk_rook"],
            ["blk_pawn", "blk_pawn",   "blk_pawn",   "blk_pawn",  "blk_pawn", "blk_pawn",   "blk_pawn",   "blk_pawn"],
            ["",         "",           "",           "",          "",         "",           "",           ""        ],
            ["",         "",           "",           "",          "",         "",           "",           ""        ],
            ["",         "",           "",           "",          "",         "",           "",           ""        ],
            ["",         "",           "",           "",          "",         "",           "",           ""        ],
            ["wht_pawn", "wht_pawn",   "wht_pawn",   "wht_pawn",  "wht_pawn", "wht_pawn",   "wht_pawn",   "wht_pawn"],
            ["wht_rook", "wht_knight", "wht_bishop", "wht_queen", "wht_king", "wht_bishop", "wht_knight", "wht_rook"]
        ]