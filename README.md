# Coinfection
This is coinfections core code, details about coinfection can be found at https://coof.live

## Compiling
Binarys are available at at https://github.com/Coinfection-Project/coinfection/releases/latest however we recommend you self compile.

### Requirements
You will need python 3.6 upwards, the latest pip and git.

### Ubuntu
First download the code:
```
git clone -b master https:/github.com/coinfection-project/coinfection 
cd coinfection
```
Now install the dependency's:
```
pip3 install -r requirements.txt
```
If you are on a low power device such as a rpi then use 
```
pip3 install -r requirements.txt --no-cache-dir
```
To reduce ram usage. 
Now we run the code
There are 4 main aspect to this codebase:
coof-node.py: The server that syncs and validates blockchains, needed for mining and infecting
coof-wallet-api.py: The wallet api, also provides a basic cli interface to send transactions. Needs to connect to a public node or a local coof-node
coof-wallet-gui.py: The gui using pygame, requires coof-wallet-api to be running
coof-miner.py: The cli solominer for coinfection, requires a local coof-node or a public node. If you have coof-wallet-api running locally it will auto configure and mine without any manual setup.

Please run any of these using the following command:
```
python3 src/<NAME>.py
```
eg:
```
python3 src/coof-node.py
```
<b> Do NOT run any of the programs in the IDE as they use parallel programing which the IDE does not support</b>

### Copyright
Any file we touch must have the following copyright statement at the top
```python
'''
 (c) 2020 Coinfection Project
 This code is licensed under the GNU General Public License v3.0 (see LICENSE.txt for details)
'''
```
If you include code from another project or stack overflow please provide a link to the file and loc, eg:
```
```python
'''
Improved bit sorting algo.
Sourced from example-coin:
https://github.com/example-project/example-coin/blob/master/src/bit-sort.py#L3542
'''
```
### Pull Requests
Pull Requests are welcomed, please ensure you make unit tests for new code and ensure it is being merged into the development branch. Please update the version to the version formatting defined in the 'Version Format' section. If the pr is fixing a bug please ensure a issue has already been opened with the bug report and has been seen by a developer and marked with the "will fix" tag. Any issue that does not fulfill this criterion will be closed.
### Version Format
We use a modified major breaking minor version system. 
the first digit is major, he second is breaking and the third is minor. All minor releases should be backwards compatible. breaking releases may or may not need a hard fork and major releases are mandatory (will result in a local chain split if you do not upgrade) and require at least 2 weeks before the fork date.
EG:
```ver 402``` is version 4.0.2. Please ensure you update the config.py and forks.py with the version.
