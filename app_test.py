import requests

ec2_address = 'http://ec2-34-245-112-242.eu-west-1.compute.amazonaws.com'
# reply = requests.get('http://ec2-34-240-23-210.eu-west-1.compute.amazonaws.com/index')
# print(reply.content)

reply = requests.post('{}/get_text?filename=that-feels-really-powerful.wav'.format(ec2_address))
print(reply.content)