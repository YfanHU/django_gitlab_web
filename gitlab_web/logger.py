import os
import time

class Logger():
    def __init__(self):
        self.log_dir='log/'
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)
        # TODO 判断是否太多文件，删除多余文件
        print('init log')
    def add_log(self,log_info):
        today=time.strftime("%Y-%m-%d", time.localtime(time.time()))
        log_file_name='.'.join([today,'txt'])
        print(log_file_name)
        with open(self.log_dir+log_file_name,'w+',encoding='utf-8') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(log_info+'\n'+content)

    def show_log(self):
        log_files = sorted(os.listdir(self.log_dir),reverse=True)
        reponse = ['<ul>', '</ul>']
        row = ['<li>', '</li>']
        res = ''
        try :
            print(self.log_dir+log_files[0],os.path.exists(self.log_dir+log_files[0]))
            with open(self.log_dir+log_files[0],'r',encoding='utf-8') as f:
                s = []
                for _ in range(10):
                    next_line = f.readline()
                    if next_line:
                        s.append(next_line)
                    else :
                        break
            for i in s:
                res+=i.strip().join(row)
            return res.join(reponse)
        except :
            return '<ul></ul>'

if __name__=='__main__':
    log=Logger()
    log.add_log('132')
    log.add_log('321')
    log.show_log()
