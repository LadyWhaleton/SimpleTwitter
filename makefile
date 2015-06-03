default:
	echo 'hi'
	
getFT:
	scp stong002@tango-9.cs.ucr.edu:~/Downloads/finalTopol.py finalTopol.py

topo:
	sudo mn --custom finalTopol.py --topo mytopo
