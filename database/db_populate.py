
from db_session import *


def main():
	# populate db with following data

	category = Category(name = "Football")
	Item1 = Item(
		name = "Ball",
		description = """A foot-ball is a ball inflated with air that is used to play one of the various sports known as football. In these games, with some exceptions, goals or points are scored only when the ball enters one of two designated goal-scoring areas; football games involve the two teams each trying to move the ball in opposite directions along the field of play.""",
		category = category)
	Item2 = Item(
		name = "Goal",
		description = """In association football the goal is the only method of scoring. It is also used to refer to the scoring structure. An attempt on goal is referred to as a "shot". To score a goal, the ball must pass completely over the goal line between the goal posts and under the crossbar and no rules may be violated on the play (such as touching the ball with the hand or arm).""",
		category = category)
	Item3 = Item(
		name = "Pitch",
		description = """A pitch or a sports ground is an outdoor playing area for various sports. The term pitch is most commonly used in British English, while the comparable term in American and Canadian English is playing field or sports field.""",
		category = category)
	db_session.add(category)
	db_session.add(Item1)
	db_session.add(Item2)
	db_session.add(Item3)


	category = Category(name = "Car")
	Item1 = Item(
		name = "Tire",
		description = """A tire (American English) or tyre (British English; see spelling differences) is a ring-shaped component that surrounds a wheel's rim to transfer a vehicle's load from the axle through the wheel to the ground and to provide traction on the surface traveled over. Most tires, such as those for automobiles and bicycles, are pneumatically inflated structures, which also provide a flexible cushion that absorbs shock as the tire rolls over rough features on the surface. Tires provide a footprint that is designed to match the weight of the vehicle with the bearing strength of the surface that it rolls over by providing a bearing pressure that will not deform the surface excessively.""",
		category = category)
	Item2 = Item(
		name = "Steer Wheel",
		description = """A steering wheel is a wheel that turns to change the direction of a vehicle""",
		category = category)
	Item3 = Item(
		name = "Windshield",
		description = """The windshield (North American English) or windscreen (Commonwealth English) of an aircraft, car, bus, motorbike or tram is the front window, which provides visibility whilst protecting occupants from the elements. Modern windshields are generally made of laminated safety glass, a type of treated glass, which consists of, typically, two curved sheets of glass with a plastic layer laminated between them for safety, and bonded into the window frame.""",
		category = category)
	db_session.add(category)
	db_session.add(Item1)
	db_session.add(Item2)
	db_session.add(Item3)


	category = Category(name = "Computer")
	Item1 = Item(
		name = "Monitor",
		description = """A computer monitor is an output device that displays information in pictorial form. A monitor usually comprises the display device, circuitry, casing, and power supply. The display device in modern monitors is typically a thin film transistor liquid crystal display (TFT-LCD) with LED backlighting having replaced cold-cathode fluorescent lamp (CCFL) backlighting. Older monitors used a cathode ray tube (CRT). Monitors are connected to the computer via VGA, Digital Visual Interface (DVI), HDMI, DisplayPort, Thunderbolt, low-voltage differential signaling (LVDS) or other proprietary connectors and signals.""",
		category = category)
	Item2 = Item(
		name = "Keyboard ",
		description = """In computing, a computer keyboard is a typewriter-style device which uses an arrangement of buttons or keys to act as mechanical levers or electronic switches. Following the decline of punch cards and paper tape, interaction via teleprinter-style keyboards became the main input method for computers.""",
		category = category)
	Item3 = Item(
		name = "Motherboard",
		description = """A motherboard (sometimes alternatively known as the main circuit board, system board, baseboard, planar board or logic board, or colloquially, a mobo) is the main printed circuit board (PCB) found in general purpose computers and other expandable systems. It holds and allows communication between many of the crucial electronic components of a system, such as the central processing unit (CPU) and memory, and provides connectors for other peripherals. Unlike a backplane, a motherboard usually contains significant sub-systems such as the central processor, the chipset's input/output and memory controllers, interface connectors, and other components integrated for general purpose use and applications.""",
		category = category)
	Item4 = Item(
		name = "Central processing unit",
		description = """A central processing unit (CPU), also called a central processor or main processor, is the electronic circuitry within a computer that carries out the instructions of a computer program by performing the basic arithmetic, logic, controlling, and input/output (I/O) operations specified by the instructions. The computer industry has used the term "central processing unit" at least since the early 1960s. Traditionally, the term "CPU" refers to a processor, more specifically to its processing unit and control unit (CU), distinguishing these core elements of a computer from external components such as main memory and I/O circuitry.""",
		category = category)
	db_session.add(category)
	db_session.add(Item1)
	db_session.add(Item2)
	db_session.add(Item3)
	db_session.add(Item4)


	db_session.commit()

	print("\nDatabase has been populated with initial data\n")


if __name__ == '__main__':
	main()
