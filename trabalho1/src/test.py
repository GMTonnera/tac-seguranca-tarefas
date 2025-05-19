import requests


def test1():
    headers = {
                "Authorization": f"Bearer 81267985c250d68569cde00ccc43428d7bd50e1902882c3b2bb99df8ec2b951f"
    }
    
    response = requests.get(f'http://localhost:8000/contacartao/1/info', headers=headers)
    
    print(">>>", response.json()['Message'], response.json()['Error'])            

if __name__ == "__main__":
    test1()