import argparse

parser = argparse.ArgumentParser()
parser.add_argument('txt_file', help='''---
File to upload should be txt in following format:
192.168.0.0/20,test,eve ---''')
args = parser.parse_args()
txt_file = args.txt_file


class SubNCalc:

    def __init__(self):
        self.user_input = txt_file
        self.save_file()

    def open_file(self):
        try:
            with open(self.user_input, "r") as sub_net_list:
                sub_net_list = sub_net_list.readlines()
                sub_net_list = [x.rstrip('\n') for x in sub_net_list]
                new_list = []
                for line in sub_net_list:
                    if len(line) < 1 or line.startswith(' '):
                        pass
                    else:
                        new_list.append(line)
                return new_list
        except FileNotFoundError:
            print("Please checks if file is in directory")

    def up_to_eight(self, power, sn_list):
        sn_list = sn_list[0].split('.')
        sn = [int(x) for x in sn_list]
        ip_list = []
        power = power
        max_numb = (2 ** power) - 1
        num_list = [x for x in range(sn[3] + 1, max_numb + sn[3])]
        for x in num_list:
            ip_list.append(str(sn[0]) + '.' + str(sn[1]) + '.' + str(sn[2]) + '.' + str(x))
        return ip_list

    def below_sixteen(self, power, sn_list):
        sn_list = sn_list[0].split('.')
        sn = [int(x) for x in sn_list]
        ip_list = []
        power = power
        power_r = power - 8
        max_numb = (2 ** power_r)
        last_num_list = [x for x in range(0, 256)]
        tir_num_list = [x for x in range(sn[2], max_numb + sn[2])]
        for x in tir_num_list:
            for z in last_num_list:
                ip_list.append(str(sn[0]) + '.' + str(sn[1]) + '.' + str(x) + '.' + str(z))
        ip_list.pop()
        ip_list = ip_list[1::]
        return ip_list

    def above_sixteen(self, power, sn_list):
        sn_list = sn_list[0].split('.')
        sn = [int(x) for x in sn_list]
        ip_list = []
        power = power
        power_r = power - 16
        max_numb = (2 ** power_r)
        last_num_list = [x for x in range(0, 256)]
        tir_num_list = [x for x in range(0, 256)]
        sec_num_list = [x for x in range(sn[1], max_numb + sn[1])]
        for c in sec_num_list:
            for x in tir_num_list:
                for z in last_num_list:
                    ip_list.append(str(sn[0]) + '.' + str(c) + '.' + str(x) + '.' + str(z))
        ip_list.pop()
        ip_list = ip_list[1::]
        return ip_list

    def sub_net_mask(self):
        sub_list = self.open_file()
        if sub_list:
            s = [x.replace('/', ',') for x in sub_list]
            sn_length = [x.split(',') for x in s]
            all_ip_list = []
            for x in sn_length:
                if len(x) != 4:
                    print('incorrect input in txt file')
                    break
                else:
                    for y in sn_length:
                        power = 32 - int(y[1])
                        if power <= 8:
                            a = self.up_to_eight(power, y)
                            for p in a:
                                all_ip_list.append(p + ',' + y[2] + ',' + y[3])
                        elif 8 < power <= 16:
                            a = self.below_sixteen(power, y)
                            for n in a:
                                all_ip_list.append(n + ',' + y[2] + ',' + y[3])
                        elif power > 16:
                            a = self.above_sixteen(power, y)
                            for k in a:
                                all_ip_list.append(k + ',' + y[2] + ',' + y[3])
                        else:
                            print("Oops, something went wrong..")
            return all_ip_list
        else:
            print('The txt file is incorrect')
            return False

    def save_file(self):
        with open('my_list.csv', 'w+') as my_file:
            titles = 'ip_address,reason,requested_by'
            my_file.write(titles)
        inner_list = self.sub_net_mask()
        if inner_list:
            with open('my_list.csv', 'a+') as my_file:
                my_file.write('\n')
                for x in inner_list:
                    my_file.write(x)
                    my_file.write('\n')
                print("File created - my_list.csv")
                return my_file
        else:
            pass


SubNCalc()

