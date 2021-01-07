from requests import get

class Shared():
    def __init__(self, token, users, parameters):
        self.token = token
        self.users = users
        self.parameters = parameters
        self.data=self.getshared(self.users)
        self.table=self.gentable(self.data, self.users)
        # self.formatted=self.filter(self.table)
        # self.formatted=self.format_table(self.formatted)
        self.formatted=self.format_table(self.table)

    def getanime(self, user, token):
        headers = {
            'Authorization': 'Bearer '+token
        }
        parameters='&'.join(['='.join(i) for i in self.parameters.items()])
        
        r=get(f"https://api.myanimelist.net/v2/users/{user}/animelist?{parameters}", headers=headers)
        return r

    def getshared(self, users):
        shared={}
        errors={}
        for user in users:
            r=self.getanime(user, self.token)
            if r.status_code==200:
                r=r.json()
                for i in r['data']:
                    if i['node']['title'] not in shared:
                        shared[i['node']['title']]={
                            'data': {},
                            'id': i['node']['id'],
                            'main_picture': i['node']['main_picture']
                        }

                    shared[i['node']['title']]['data'][user]=i['list_status']
            else:
                errors[user]=[r.status_code,r.json()]
        
        return shared, errors


    # quick helper
    def _avg(self, x):
        try:
            return sum(x)/len(x)
        except ZeroDivisionError:
            return ''

    def gentable(self, data, users):
        table=[['Title']]
        users=[i for i in users if i not in data[1]]
        table[0]+=users
        table[0].append('average score')
        # generate table template
        for i in data[0]:
            row=[i]+['']*len(users)
            i=data[0][i]
            # generate row template
            for p in i['data']:
                if i['data'][p]['score']==0:
                    row[users.index(p)+1]='ptw'
                else:
                    row[users.index(p)+1]=i['data'][p]['score']
            row.append(self._avg([i for i in row if isinstance(i, int)]))
            
            table.append(row)

        return table

    def format_table(self, table):
        # gets # of columns, adds lengths of each row/column, adds max to lengths list
        # to figure out how much whitespace needs to be added
        # (kinda really relies on monospace font)

        # i think i could do in one line but idrk
        lengths=[]
        for ci in range(len(table[0])):
            x=[]
            for r in table:
                x.append(len(str(r[ci])))
            lengths.append(max(x))

            for r in table:
                r[ci]=f'{str(r[ci]):^{lengths[ci]}}'

        table=['|'.join([str(a) for a in i]) for i in table]
        return table

    def filter(self, table, minimum):
        # filter hack for filtering lists with only ptw
        # for r in table:
        #     if not r[-1]:
        #         table.remove(r)

        
        # once i start adding variable metrics, this wont be okay
        for r in table[1:]:
            if sum([1 for i in r[1:-1] if isinstance(i, int)])<minimum:
                table.remove(r)
        
        return table

def gettoken():
        from sys import exit

        from auth import Auth
        a=Auth()
        print("open the following link, allow access, and paste the redirect link here")
        print(a.getlink())
        code = input().split('code=')[-1]
        token = a.gettoken(code)

        # with open('config.py', 'r+') as config:
        #     temp=config.read().split("\n")
        #     temp[-1]=f"token={token}"
        #     config.write("\n".join(temp))

        print(token)
        print("paste above token into config.py and restart")
        exit()

if __name__ == "__main__":
    try:
        from config import token
    except ImportError:
        gettoken()

    parameters = {
        'fields': 'list_status',
        'sort': 'anime_title',
        'limit': '3'
    }
    users=[]

    # responses=getanime(token, parameters, users)
    # print([r.status_code for r in responses])
    # shared=getshared(responses)
    # table=gentable(shared, users)
    # # table=filter(table)
    # table=format_table(table)

    shared=Shared(token, users, parameters)

    with open('output.txt', 'w+', encoding='utf-8') as output:
        for i in shared.formatted:
            output.write(str(i)+'\n')

print()
