using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class TextController : MonoBehaviour
{

	public Text text;

	private enum States
	{
		coast, cave, river, reefRocks, skeleton, sea
	};

	private States myState;
	private bool rope = false;
	private bool raft = false;

	// Use this for initialization
	void Start () {
		myState = States.coast;
	}
	
	// Update is called once per frame
	void Update() {
		switch (myState)
		{
			case States.coast:
				stateCoast();
				break;
			case States.cave:
				stateCave();
				break;
			case States.river:
				stateRiver();
				break;
			case States.reefRocks:
				stateReefRocks();
				break;
			case States.skeleton:
				stateSkeleton();
				break;
			case States.sea:
				stateSea();
				break;
			default:
				stateCoast();
				break;
		}
	}

	void stateCoast(){
		if (!raft) {
			text.text = "You are on a small prison island rounded by sharp shallow rocks. " +
			            "You want to escape. There are a small river to the north, " +
			            "some reef rocks by the coast, and the cave west to the river.\n\n" +
			            "Press C to investigate Cave\n" +
			            "Press I to investigare rIver\n" +
			            "Press R to investigate Reef rocks\n";
			if (Input.GetKeyDown(KeyCode.C)) {
				myState = States.cave;
			}
			else if (Input.GetKeyDown(KeyCode.I)) {
				myState = States.river;
			}
			else if (Input.GetKeyDown(KeyCode.R)) {
				myState = States.reefRocks;
			}
		}
		else {
			text.text = "Now, when you found a raft, you finally can sail off the island.\n\n" +
			            "Press S to sail from the prison island\n" +
			            "Press C to investigate Cave\n" +
			            "Press I to investigare rIver\n" +
			            "Press R to investigate Reef rocks\n";
			if (Input.GetKeyDown(KeyCode.S)) {
				myState = States.sea;
			}
			if (Input.GetKeyDown(KeyCode.C)) {
				myState = States.cave;
			}
			else if (Input.GetKeyDown(KeyCode.I)) {
				myState = States.river;
			}
			else if (Input.GetKeyDown(KeyCode.R)) {
				myState = States.reefRocks;
			}
		}
	}

	void stateCave() {
		if (raft) {
			text.text = "No more interesting things here.\n\n" +
			            "Press C to return to the Coast\n";
			if (Input.GetKeyDown(KeyCode.C)) {
				myState = States.coast;
			}
		} 
		else if (!rope) {
			text.text = "You are at the enter to the deep, deep cave. There's definitely " +
			            "something on the bottom, but you're not going to make it " +
			            "without some rope.\n\n" +
			            "Press C to return to the Coast\n";
			if (Input.GetKeyDown(KeyCode.C)) {
				myState = States.coast;
			}
		}
		else {
			text.text = "You are at the enter to the deep, deep cave. There's definitely " +
			            "something on the bottom. Recently you found a rope, so you can " +
			            "give it a try. \n\n" +
			            "Press D to hang Down the cave\n" +
			            "Press C to return to the Coast\n";
			if (Input.GetKeyDown(KeyCode.D)) {
				myState = States.skeleton;
			}
			if (Input.GetKeyDown(KeyCode.C)) {
				myState = States.coast;
			}
		}
	}

	void stateRiver() {
		if (!raft) {
			text.text = "Thanks to that river you have something to drink, but nothing more.\n\n" +
			            "Press C to return to the Coast\n";
			if (Input.GetKeyDown(KeyCode.C)) {
				myState = States.coast;
			}
		}
		else {
			text.text = "You took some water to have something to drink before you reach steady land.\n\n" +
			            "Press C to return to the Coast\n";
			if (Input.GetKeyDown(KeyCode.C)) {
				myState = States.coast;
			}
		}
}

	void stateReefRocks() {
		if (!rope) {
			text.text = "When you're getting closer, you see something tangled into reef. It's a rope! \n\n" +
			            "Press C to return to the Coast\n";
			if (Input.GetKeyDown(KeyCode.C)) {
				rope = true;
				myState = States.coast;
			}
		}
		else {
			text.text = "No more interesting things here.\n\n" +
			            "Press C to return to the Coast\n";
			if (Input.GetKeyDown(KeyCode.C)) {
				myState = States.coast;
			}
		}
	}

	void stateSkeleton(){
		text.text = "When you reached the bottom of the cave, you found the skeleton of a poor men " +
		            "and emergency raft nearby. Now you can leave the island!\n\n" +
		            "Press C to return to the Coast";
		if (Input.GetKeyDown(KeyCode.C)) {
			myState = States.coast;
			raft = true;
			
		}
	}
	
	void stateSea(){
		text.text = "You win\n\n" +
		            "Press S to Start again";
		if (Input.GetKeyDown(KeyCode.S)) {
			myState = States.coast;
			raft = false;
			rope = false;
		}
	}
}