

class OddsMath:

    @staticmethod
    def implied_prob(num, format = "decimal"):
        if (format == "decimal"):
            return OddsMath._decimal_implied_prob(num)
        elif (format == "american"):
            return OddsMath._american_implied_prob(num)


    @staticmethod
    def _decimal_implied_prob(num):
        return 1.0 / num
    
    
    @staticmethod 
    def _american_implied_prob(num):
        if (num > 0):
            return 100 / (num + 100)
        else:
            return num / (num + 100)


    # @staticmethod
    # def total_implied_prob(nums):
    #     total = 0
    #     for num in nums:
    #         total += OddsMath.implied_prob(num)

    # @staticmethod
    # def bet_from_collect(num, collect):
    #     if (num > 0):
    #         return (100 * profit) / num
    #     else:
    #         return (num * profit) / 100

    # @staticmethod
    # def hedge(nums, bet):
    #     ips = [OddsMath.implied_probs(num) for num in nums]
    #     total_ip = OddsMath.total_implied_probs(nums)
    #     ip_ratios = [ip / total_ip for ip in ips]
    #     return [bet * ratio for ratio in ip_ratios]