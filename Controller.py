from Session import Session
import pygame
import pygame_gui
class Controller:
	sessionList = []
	pygame.init()
	pygame.display.set_caption('Quick Start')
	window_surface = pygame.display.set_mode((1300, 800))
	manager = pygame_gui.UIManager((1300, 800))
	clock =  pygame.time.Clock()
	currentSession = 0
	session_button = None
	rmse_button = None
	flick_button = None
	replay_button = None
	accuracy_text = None
	mean_loss_text = None
	mean_loss = None
	def createSession(self, target_radius, simLen, numTargets):
		s = Session(target_radius, simLen, numTargets)
		self.sessionList.append(s)

	def executeSession(self, session_number):
		# session_number is just the session to bee executed's index in the list
		self.sessionList[session_number].runSession()

	def menu(self):
		self.background = pygame.Surface((1300, 800))
		self.background.fill((255, 255, 255))

		self.submit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1000, 720), (100, 30)), text='Start', manager=self.manager)

		self.size_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((140, 310), (300, 20)), text = 'Radius of Target ([10 - 70] pixels)', manager = self.manager)
		self.radius_value_range = [10, 70]
		# slider for the radius_size
		self.size_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((30, 340), (550, 20)), start_value=10, value_range=self.radius_value_range, manager = self.manager)

		self.targets_value_range = [1, 10]
		# slider for the number of targets
		self.targets_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((130, 460), (320, 20)), text = 'Number of Targets on Screen ([1 - 10])', manager = self.manager)
		self.targets_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((30, 490), (550, 20)), start_value=1, value_range=self.targets_value_range, manager = self.manager)

		self.sim_value_range = [10, 120]
		# slider for sim length
		self.sim_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((130, 610), (320, 20)), text = 'Length of Session ([10 - 120] seconds)', manager = self.manager)
		self.sim_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((30, 640), (550, 20)), start_value=10, value_range=self.sim_value_range, manager =self. manager)
		#name
		self.name_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((440, 720), (280, 20)), text = 'Made by Avi Vadali', manager = self.manager)
		pygame.display.update()

	#logo
	def setupScreen(self):
		title_text = pygame.image.load('aim_trainer_title.png')
		n1_logo = pygame.image.load('n1_logo.png')
		powered_by = pygame.image.load('powered_by.png')
		self.window_surface.blit(n1_logo, (700, 130))
		self.window_surface.blit(powered_by, (200, 150))
		self.window_surface.blit(title_text, (50, 0))
		pygame.display.update()
		self.clock = pygame.time.Clock()

# Things in the second menu:
# - create a session
# - get rmse plot of previous Session
# - get flicking data
# - get Session 'replay' to trace out the Cursor's paths
	def secondMenu(self):
		self.background = pygame.Surface((1300, 800))
		self.background.fill((255, 255, 255))
		# title text for the menu
		menu_text = pygame.image.load('session_menu.png')
		self.window_surface.blit(menu_text, (350, 15))
		# buttons that this menu will have
		# session_button has been configured
		self.session_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 200), (400, 60)), text='Create a New Session', manager=self.manager)
		#self.flick_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 300), (400, 60)), text='Get Mouse Flicking Data', manager=self.manager)
		self.replay_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 400), (400, 60)), text='Get Mouse Path Replay', manager=self.manager)
		self.rmse_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 600), (400, 60)), text='Get RMSE Time Series', manager=self.manager)
		self.accuracy_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 150), (320, 20)), text = 'User \'s clicking accuracy', manager = self.manager)
		self.mean_loss_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((900, 150), (320, 20)), text = 'Mean loss between targets', manager = self.manager)
		self.mean_loss = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((900, 250), (320, 20)), text = self.sessionList[self.currentSession - 1].getMeanLoss(), manager = self.manager)
		self.accuracy_disp = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 250), (320, 20)), text = self.sessionList[self.currentSession - 1].getAccuracy(), manager = self.manager)
		pygame.display.update()
		# self.menu()
		# self.setupScreen()
	def runController(self):
		is_running = True
		self.menu()
		self.setupScreen()
		while is_running:
			time_delta = self.clock.tick(60)/1000.0
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					is_running = False
				if event.type == pygame.USEREVENT:
					if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
						if event.ui_element == self.session_button:
							# essentially hiding the second menu
							self.session_button.hide()
							#self.flick_button.hide()
							self.replay_button.hide()
							self.rmse_button.hide()
							self.accuracy_text.set_dimensions((0, 0))
							self.mean_loss_text.set_dimensions((0, 0))
							self.accuracy_disp.set_dimensions((0, 0))
							self.mean_loss.set_dimensions((0, 0))
							self.name_text.set_dimensions((0, 0))
							self.window_surface.blit(self.background, (0, 0))
							pygame.display.update()
							# rerunning the controller
							self.runController()
						if event.ui_element == self.rmse_button:
							self.sessionList[self.currentSession - 1].plotRMSE()
						if event.ui_element == self.replay_button:
							self.sessionList[self.currentSession - 1].replays()
						#if event.ui_element == self.flick_button:
						# if event.ui_element == self.replay_button:

						if event.ui_element == self.submit_button:
							# get the values of the sliders
							radius = self.size_slider.get_current_value()
							num_targets = self.targets_slider.get_current_value()
							sim_len = self.sim_slider.get_current_value()
							# spawn_delay = delay_slider.get_current_value()
							# hide the sliders
							self.size_slider.hide()
							self.targets_slider.hide()
							self.sim_slider.hide()
							# delay_slider.hide()
							# hide the text
							self.size_text.set_dimensions((0, 0))
							self.targets_text.set_dimensions((0, 0))
							self.sim_text.set_dimensions((0, 0))
							self.name_text.set_dimensions((0, 0))
							# delay_text.set_dimensions((0, 0))
							# hide the submit_button
							self.submit_button.hide()
							self.window_surface.blit(self.background, (0, 0))
							# create a new Session with all of the user's preferred settings
							self.createSession(radius, sim_len, num_targets)
							print('Session created')
							# exit the loop
							self.is_running = False
							print('Session executed')
							self.executeSession(self.currentSession)
							# this method will display the second menu
							c.secondMenu()
							self.currentSession += 1
							self.sessionList[self.currentSession - 1].computeFlickings()
				self.manager.process_events(event)

			self.manager.update(time_delta)

			self.manager.draw_ui(self.window_surface)

			pygame.display.update()






c = Controller()
c.runController()
