var store = [{
        "title": "Workflow",
        "excerpt":"Workflow Overview This takes in the intial arguments and runs everything from concise in the correct order. Steps: Reading tsv’s Converts whole percentages to decimal if needed. Imports the canopus match information (works for both tsv and csv) Renames the in silico columns as needed and captures both the most...","categories": [],
        "tags": [],
        "url": "/%7B%7D/Workflow/",
        "teaser": null
      },{
        "title": "Codeoverview",
        "excerpt":"Overview All of the classes to run concise are in conCISE.py; these functions are run through the workflowMain.py. Both the GUI and myBinder use the CLI to initiate the workflow with the correct files. Code (src/) Graphical User Interface: conciseGui.py Command Line Interface:conciseCLI.py myBinder Interface: conciseBinder.ipynb ConCISE functions: conCISE.py ConCISE...","categories": [],
        "tags": [],
        "url": "/%7B%7D/codeOverview/",
        "teaser": null
      },{
        "title": "Commandlineinterface",
        "excerpt":"Command Line Interface and myBinder (conciseCLI.py, conciseBinder.ipynb) This is the main workflow runner that all other methods will utilize. To use the CLI you will need to download the source code. The CLI code will run the workflow runner in the main workflow python file. To run the myBinder click...","categories": [],
        "tags": [],
        "url": "/%7B%7D/commandLineInterface/",
        "teaser": null
      },{
        "title": "Concisefunctions",
        "excerpt":"conCISE functions (conCISE.py) Classes: getJob mergeAnnotations weightEdges makeNet selectAnnotation getJob This will utilize the GNPS API to pull either the GNPS library matches or GNPS analog matches. When more functionality is added to the GNPS API this will be incorporated into conCISE to pull all needed dataframes and not just...","categories": [],
        "tags": [],
        "url": "/%7B%7D/conciseFunctions/",
        "teaser": null
      },{
        "title": "Graphicaluserinterface",
        "excerpt":"Graphical User Interface Classes: emittingStream mainWindow emittingStream This is a QObject which excepts pyqtSignals and can emit the signal into text. This allows us to capture any messages sent to the console and write it to the text box in the GUI itself. mainWindow Main window of the widget which...","categories": [],
        "tags": [],
        "url": "/%7B%7D/graphicalUserInterface/",
        "teaser": null
      },{
        "title": "Guiwidgets",
        "excerpt":"Custom Widgets  fileSearch  A search widget which allows the user to select specific files in their local computer.   dirSearch  A search widget which allows the user to select specific directories in theier local computer   iconLbel  A help icon and label for each bar in the GUI  ","categories": [],
        "tags": [],
        "url": "/%7B%7D/guiWidgets/",
        "teaser": null
      },]
