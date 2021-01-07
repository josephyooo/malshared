from requests import get

def getshared(token, parameters, users):
    headers = {
        'Authorization': 'Bearer '+token
    }
    parameters='&'.join(['='.join(i) for i in parameters.items()])
    shared={}
    errors={}
    for user in users:
        r=get(f"https://api.myanimelist.net/v2/users/{user}/animelist?{parameters}", headers=headers)

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

# quick helper
def avg(x):
    try:
        return sum(x)/len(x)
    except ZeroDivisionError:
        return 'n/a'

def gentable(shared, users):
    table=[['Title']]
    users=[i for i in users if i not in shared[1]]
    table[0]+=users
    table[0].append('average score')
    # generate table template
    for i in shared[0]:
        row=[i]+['']*len(users)
        i=shared[0][i]
        # generate row template
        for p in i['data']:
            if i['data'][p]['score']==0:
                row[users.index(p)+1]='ptw'
            else:
                row[users.index(p)+1]=i['data'][p]['score']
        row.append(avg([i for i in row if isinstance(i, int)]))
        
        table.append(row)

    # table=['|'.join([str([a for a in i])]) for i in table]
    return table

def format_table(table):
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

if __name__ == "__main__":
    try:
        from config import token
    except ImportError:
        gettoken()

    parameters = {
        'fields': 'list_status',
        'sort': 'anime_title',
        'limit': '10'
    }

    shared=getshared(token, parameters, users)
    table=gentable(shared, users)
    table=format_table(table)

    # for i in table: print(i)
    with open('output.txt', 'w+', encoding='utf-8') as output:
        for i in table: output.write(str(i)+'\n')

print()