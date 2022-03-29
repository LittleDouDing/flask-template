class Config:
    @staticmethod
    def port_regex():
        regex1 = r'^(GigabitEthernet\d+/0/\d+|XGigabitEthernet\d+/0/\d+|Ten-GigabitEthernet\d+/0/\d+|Eth-Trunk\d+|'
        regex2 = r'gei-0/\d+/0/\d+|xgei-0/\d+/0/\d+|gei_\d+/\d+|xgei_\d+/\d+|smartgroup\d+)$'
        return regex1 + regex2

    @staticmethod
    def route_regex():
        ip = r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}'
        ip_regexp1 = '^掩码：' + ip + '\n网关：' + ip + r'\nDNS\(主\)：' + ip + r'\nDNS\(备\)：' + ip + '$'
        ip_regexp2 = '^掩码：' + ip + '\n网关：' + ip + '\nDNS：' + ip + '$'
        return ip_regexp1 + '|' + ip_regexp2

    @staticmethod
    def places():
        return ['霞山', '赤坎', '麻章', '开发区', '坡头', '东海', '吴川', '遂溪', '廉江', '徐闻', '雷州']

    @staticmethod
    def manufactures():
        return ['华为', '中兴', '华三', '思科', '烽火']
