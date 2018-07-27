# typistid
Program that attempts to fingerprint user's typing habits

To record keystroke data:
  1. Open keystroke-recorder/recorder.html in your browser
  2. Type something into the input box and click "Enter" when finished.
  3. Copy the printed JSON data into a file

To compare keystrokes to two existing data files:<br>
  Example usage: <code>python profiler.py compare data1.json data2.json new_data.json</code>
  
To visualize data:<br>
  Example usage: <code>python profiler.py visualize my_keystroke_data.json</code><br>
  Example output: ![alt text](https://raw.githubusercontent.com/christianwang0x/typistid/master/keys.png)
