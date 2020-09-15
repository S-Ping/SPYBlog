__author__ = 'SPing'


"""用于生成随机验证码"""
import string
import random


class RandomStr:

    @staticmethod
    def random_seq(choice_seq, count=6, repeatable=True):
        """
        生成随机数列表
        :param choice_seq:list,
        :param count: int,随机数长度
        :param repeatable: bool,是否可重复
        :return: list
        """
        if repeatable:
            return [random.choice(choice_seq) for _ in range(count)]
        return random.sample(choice_seq, count)

    def captcha(self):
        '''
        生成随机数字验证码
        '''
        digits = self.random_seq(string.digits)
        random.shuffle(digits)
        return ''.join(digits)

    def password(self, count=8):
        '''
        生成随机八位初始密码
        '''
        while True:
            passwd = self.random_seq(string.digits + string.ascii_letters, count)
            set1 = set(string.ascii_uppercase).intersection(passwd)
            set2 = set(string.ascii_lowercase).intersection(passwd)
            set3 = set(string.digits).intersection(passwd)
            if set1 and set2 and set3:
                return ''.join(passwd)

if __name__ == '__main__':
    c = RandomStr()
    print(c.password())
