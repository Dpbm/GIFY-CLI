from constants import colors
import emoji 


async def check_input_args(inputs):
    if len(inputs) - 1 > 2 or len(inputs) - 1 < 2:
        emojis = f'{colors.FAIL}{emoji.emojize(":cross_mark:  :warning:")}'
        text1 = f"{colors.FAIL}Usage: python src/main.py link output_file_name"
        text2 = f"{colors.FAIL}You need to pass only two arguments"
        

        out_emoji = emojis.center(len(text1), " ")
        out_text1 = text1.center(55, " ")
        out_text2 = text2.center(len(text1), " ")

        print(out_emoji)
        print(out_text1)
        print(out_text2)
        exit(1)


        
        