import random
class CZY:
    def cannot_but():
            cannot_but_dict = {
            "香":"林襄",
            "害怕":"Linkin park",
            "被罵":"伊隆罵",
            "die":"一代一代一代",
            "沙啞":"三上悠亞",
            "發出噪音":"加藤鷹",
            "平安":"凌薹安",
            "跳舞":"陳威伍",
            "被打":"啊里不打",
            "做蛋達":"謝新達",
            }
            
            random_value = random.choice(list(cannot_but_dict.keys()))
            return f"張子儀不會{random_value} 但是{cannot_but_dict[random_value]}"