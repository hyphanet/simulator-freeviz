import re 
import string

testData="""
physical.udp=213.83.30.166:28000
identity=14475c717809d5367dda55f02f98cd9cefd30a6f28a1b14a2acce990a4b17e9f
myName=superduper
location=0.4590345916077352
testnetPort=29000
testnet=true
version=Fred,0.7,1.0,310
End
"""

testData3="""
status
physical.udp=213.83.30.166:28000
identity=14475c717809d5367dda55f02f98cd9cefd30a6f28a1b14a2acce990a4b17e9f
myName=superduper
location=0.04174255978367547
testnetPort=29000
testnet=true
version=Fred,0.7,1.0,321
End


CONNECTED    209.6.82.6:55555 mikeDOTd 0.5406312064503291 Fred,0.7,1.0,320 backoff: 5000 (0)
CONNECTED    82.32.17.1:5000 Toad #1 0.8265089106725086 Fred,0.7,1.0,321 backoff: 5000 (0)
CONNECTED    82.32.17.1:5001 Toad #2 0.7210865113995654 Fred,0.7,1.0,321 backoff: 5000 (0)
CONNECTED    83.196.106.202:3000 NextGen$_#1 0.9417684116796216 Fred,0.7,1.0,321 backoff: 5000 (0)
DISCONNECTED 128.100.171.30:4000 PVT 0.34696550532100745 Fred,0.7,1.0,305 backoff: 5000 (0)
DISCONNECTED 81.178.70.127:19114 sanity1 0.42306327680182465 Fred,0.7,1.0,310 backoff: 5000 (0)
DISCONNECTED 83.196.16.236:10001 NextGen5 0.3023100178897614 Fred,0.7,1.0,310 backoff: 5000 (0)



"""

testData2 ="""
physical.udp=82.32.17.1:5001
identity=3247b10f0b3f698a7712174d7b37b54a210356ce73fb564dd4ff19741bb64b55
myName=Toad #2
location=0.9417684116796216
testnetPort=6001
testnet=true
version=Fred,0.7,1.0,320
End


CONNECTED    213.83.30.166:28000 superduper 0.8042879816850985 Fred,0.7,1.0,320 backoff: 5000 (0)|14475c717809d5367dda55f02f98cd9cefd30a6f28a1b14a2acce990a4b17e9f
CONNECTED    82.32.17.1:5000 Toad #1 0.7495825470097687 Fred,0.7,1.0,320 backoff: 5000 (0)|21f6c377e5a5f7b4c14ca219bef9f334cf9e105503ecb54b034f28d347ad6156
CONNECTED    82.32.17.1:5002 Toad #3 0.8265089106725086 Fred,0.7,1.0,320 backoff: 5000 (0)|9bad8e6fc84bece87ebec52c838b4c718f153966a0c8c2b70faccb7dc7ad0dbd
CONNECTED    83.196.106.202:3000 NextGen$_#1 0.04941094442690597 Fred,0.7,1.0,320 backoff: 5000 (0)|72425091d95d8b463f8be45b6d6463f19de12d61bab684d9da4d7d9e62c93a6b
CONNECTED    83.233.97.28:4000 sandos 0.04174255978367547 Fred,0.7,1.0,320 backoff: 5000 (0)|3257150a6fc3a6912467e368201d1c0872dabca9697bd456f7ec9f5232d346f5
DISCONNECTED 213.10.90.196:37240 tubbie_node2 0.9243903267660739 Fred,0.7,1.0,305 backoff: 5000 (0)|7b985832b0b6326b8a949b9472c8a8a19ffce8deff0817f39b6a9237afe70e43
DISCONNECTED 66.36.135.217:3155 odonata 0.4853282117965083 Fred,0.7,1.0,294 backoff: 5000 (0)|b5eb67ff7b19393a13dbb66f8126819200897734dccd6d81761af5303182e1be
DISCONNECTED 66.36.153.156:3156 odonata #1 0.029565449588379145 Fred,0.7,1.0,307 backoff: 5000 (0)|42b950db0b4d07c0453992839292557d573662750031a53b3c2299ca53505f8e
DISCONNECTED 67.40.225.97:61523 TheSeeker 0.3902854008904836 Fred,0.7,1.0,305 backoff: 5000 (0)|e97f9e797f8608f29d4a40eff63b14d411fb47ac09f9dee0f6f3b55836bc368c
DISCONNECTED 70.81.24.164:7744 rek 0.11219091833051797 Fred,0.7,1.0,305 backoff: 5000 (0)|c238c425163075b59e5d3db20ca38defd2ecc0099409894b0d27c5db3eeefa99
"""

def parse(data):
	optionsline = re.compile('(\S+)\s*=(.+)')
	connection = re.compile('^CONNECTED\s+(\d+\.\d+\.\d+\.\d+:\d+|\S+:\d+)\s+(.+)\s+(0\.\d+)\s+(Fred\S+)\sbackoff: (\d+) \((\d+)\)\|(\S+)')

	options={}
	connections=[]
	backoffs={}

	for i in string.split(data,sep='\n'):
		op = optionsline.match(i)
		con = connection.match(i)

		if op:
			options[op.group(1).strip()]=op.group(2).strip() 
		elif con:
			di={'address': con.group(1), 'name': con.group(2), 'location' : con.group(3) , 
				'version': con.group(4), 'identity':con.group(7) }
			connections.append(di)
			assert 'identity' in options
			backoff={ 'identity': di['identity'],'backoffmax': con.group(5), 'backoffcur': con.group(6) }
			backoffs[ options['identity'] ]=backoff

		
	options['name']=options['myName']
	if 'physical.udp' in options.keys():
		options['address'] = options['physical.udp']

	return (options, connections, backoffs)


#pars = MyParser()
#(a,o) = parse(testData)
#print a
#print o
