# wordtree-electron
Simple GUI to explore wordtrees.

## To Use

To clone and run this repository you'll need [Git](https://git-scm.com) and [Node.js](https://nodejs.org/en/download/) (which comes with [npm](http://npmjs.com)) installed on your computer. Currently, the project calls the python script from [wordtree-python-cmd](https://github.com/trivedigaurav/wordtree-python-cmd) to generate the wordtree. You need to have python on your system.

By default, the tool loads [lorem.csv](lorem.csv) to build trees on. You can drag and drop another similarly formatted CSV file to analyze your text with the tool.


From your command line:

```bash
# Clone this repository
git clone https://github.com/trivedigaurav/wordtree-electron
# Go into the repository
cd wordtree-electron
# Install dependencies
npm install
# Run the app
npm start
```

Note: If you're using Linux Bash for Windows, [see this guide](https://www.howtogeek.com/261575/how-to-run-graphical-linux-desktop-applications-from-windows-10s-bash-shell/) or use `node` from the command prompt.

## Warning!
This tool is for exploration only. Do not use in production.
