import Scripts.Source.General.Managers.object_creator as object_creator_m
import Scripts.Source.General.Managers.object_picker as object_picker_m
import Scripts.Source.General.GSM.game_state as state_m
import Scripts.Source.GUI.Game.GameSM.game_sm as game_sm_m
import Scripts.Source.General.Game.level as level_m
import Scripts.Source.Physic.physics_world as physics_world_m
import Scripts.Source.General.Managers.game_event_log_manager as game_event_log_manager_m
import Scripts.Source.General.Managers.data_manager as data_manager_m
import moderngl as mgl

DT = 0.02


class Game(state_m.GameState):
    NAME = "Game"

    def __init__(self, app, gsm):
        super().__init__(gsm, app)
        self.level = None
        self.physic_world = physics_world_m.PhysicWorld(self)
        self.gizmos = None
        self.game_sm = None
        self.gui = app.gui
        self.ctx = self.app.ctx
        self.object_picker = None
        self.game_event_log_manager = None
        self.win_size = self.app.win_size
        self.client = gsm.network

        self.cumulative_time_for_send_data_to_server = 0
        self.is_synced = False
        self.synced_actions_id = []
        self.actions_to_send_server = {}

        self.user_name = "default"
        self.user_stats = {
            "kills": 0,
            "deaths": 0
        }

        self.client_stats = {}

    @property
    def fixed_delta_time(self):
        return self.app.fixed_delta_time

    @property
    def time(self):
        return self.app.time

    @property
    def delta_time(self):
        return self.app.delta_time

    def get_fps(self):
        return self.app.get_fps()

    def _load_level(self, file_path=None):
        if self.level:
            self.level.delete()
        if self.gizmos:
            self.gizmos.delete()
        # self.gizmos = []
        self.level = level_m.Level(self, self.gui)
        object_creator_m.ObjectCreator.rely_level = self.level
        object_picker_m.ObjectPicker.init(self, False)
        self.object_picker = object_picker_m.ObjectPicker
        self.level.load(file_path, is_game=True)

    def enter(self, params=None):
        self.game_sm = game_sm_m.GameSM(self.app, self.fsm)
        if params is None:
            level_path = "Levels/Base/Test.json"
            spawn_pos = (0, 1, 0)
            existing_clients = {}
            user_name = "Default"
        else:
            level_path, spawn_pos, existing_clients, user_name = params

        self._load_level(level_path)

        self.user_name = user_name

        self.physic_world.init_physic_object_by_level(self.level)
        self.physic_world.add_default_solvers()

        self.app.grab_mouse_inside_bounded_window = True
        self.app.set_mouse_visible(False)
        self.app.set_mouse_grab(True)

        self.spawn_player(spawn_pos)

        for client_id, data in existing_clients.items():
            if client_id != self.app.network.id:
                self.init_client_wrapper_and_data(data, client_id)

        self.game_event_log_manager = game_event_log_manager_m.GameEventLogManager(self.game_sm.state)

    def exit(self):
        self.level.delete()
        self.game_sm.release()
        object_picker_m.ObjectPicker.release()
        object_creator_m.ObjectCreator.release()
        self.app.set_mouse_grab(False)
        self.app.set_mouse_visible(True)

    # Client-Server
    def get_player_client_data(self):
        return self.level.get_player_data()

    def spawn_player(self, pos):
        self.level.spawn_player(pos)

    def init_client_wrapper_and_data(self, data, client_id):
        print(data)
        self.level.create_and_spawn_client(data["pos"], client_id)
        self.client_stats[client_id] = {
            "kills": data["kills"],
            "deaths": data["deaths"],
            "name": data["name"],
        }

    def update_game_state(self, state):
        # print(state)
        for action in state["actions"]:
            match action:
                case "spawn_client":
                    if state["actions"][action]["source"] != self.app.network.id:
                        client_wrapper = self.level.client_wrappers.get(state["actions"][action]["source"])
                        if client_wrapper:
                            client_wrapper.transformation.pos = state["actions"][action]["spawn_pos"]
                            client_wrapper.rely_object.enable = True
                        else:
                            self.game_event_log_manager.add_message(f"{state["actions"][action]["name"]} connected")
                            # self.client_stats[state["actions"][action]["source"]] = {
                            #     "kills": 0,
                            #     "deaths": 0,
                            #     "name": state["actions"][action]["name"]
                            # }
                            self.init_client_wrapper_and_data(state["game_state"][state["actions"][action]["source"]],
                                                              state["actions"][action]["source"])

                        self.synced_actions_id.append(state["actions"][action]["id_action"])
                    else:
                        raise Exception(f"Twice get spawn for same player!\nthis client id = {self.app.network.id}\n"
                                        f"source, that should be spawned: {state["actions"][action]["source"]}")
                case "disconnect_client":
                    if state["actions"][action]["source"] != self.app.network.id:
                        client_wrapper = self.level.client_wrappers.get(state["actions"][action]["source"])
                        if client_wrapper:
                            source = state["actions"][action]["source"]
                            self.game_event_log_manager.add_message(
                                f"{self.client_stats[source]["name"]} leave the game")
                            del self.client_stats[state["actions"][action]["source"]]
                            self.level.delete_object(client_wrapper)
                            del self.level.client_wrappers[state["actions"][action]["source"]]
                        else:
                            raise Exception(
                                f"Attemp to disconnect non existing client!\nthis client id = {self.app.network.id}\n"
                                f"source, that should be disconnected: {state["actions"][action]["source"]}")

                        self.synced_actions_id.append(state["actions"][action]["id_action"])
                    else:
                        raise Exception(
                            f"Called disconnect with user agreement!\nthis client id = {self.app.network.id}\n"
                            f"source, that should be disconnected: {state["actions"][action]["source"]}")
                case "kill_client":
                    source = state["actions"][action]["source"]
                    if source == self.app.network.id:
                        raise Exception("Server not should send kill message to killer!")
                    source_to_kill = state["actions"][action]["source_to_kill"]
                    self.client_stats[source]["kills"] += 1

                    if source_to_kill == self.app.network.id:
                        self.user_stats["deaths"] += 1
                        self.game_event_log_manager.add_message(
                            f"{self.client_stats[source]["name"]} KILL {self.user_name}")
                        self.level.kill_player()
                    else:
                        self.client_stats[source_to_kill]["deaths"] += 1
                        self.game_event_log_manager.add_message("Somebody KILL Somebody")
                        self.level.kill_client(source_to_kill)

                    self.synced_actions_id.append(state["actions"][action]["id_action"])

        for client_guid in state["game_state"].keys():
            if client_guid != self.app.network.id and self.level.client_wrappers.get(client_guid):
                cw = self.level.client_wrappers[client_guid]
                cw.transformation.pos = state["game_state"][client_guid]["pos"]
                cw.transformation.rot = state["game_state"][client_guid]["rot"]

    ###############

    def before_exit(self):
        self.app.exit()

    def update(self):
        self.level.apply_components()
        object_picker_m.ObjectPicker.picking_pass()

    def fixed_update(self):
        self.physic_world.step(self.app.fixed_delta_time)
        self.level.fixed_apply_components()

        if self.app.network.id != -1:
            self.send_data_to_server()

    def send_data_to_server(self):
        response = {}
        response["actions"] = {}

        response["player_data"] = self.level.player_component.serialize()
        response["player_data"]["kills"] = self.user_stats["kills"]
        response["player_data"]["deaths"] = self.user_stats["deaths"]
        response["player_data"]["name"] = self.user_name

        response["actions"]['synced'] = self.synced_actions_id

        for action_key, action_values in self.actions_to_send_server.items():
            response["actions"][action_key] = action_values

        self.actions_to_send_server.clear()

        server_response = self.app.network.send(response)

        self.synced_actions_id.clear()

        self.update_game_state(server_response)

    def render_level(self):
        self.app.ctx.screen.use()
        self.ctx.clear(color=(0.08, 0.16, 0.18, 1))
        self.ctx.enable(mgl.BLEND)
        self.level.render_opaque_objects()

        self.level.render_transparent_objects()

    def render_gizmo(self):
        self.level.on_draw_gizmos()

    def render_gui(self):
        self.app.ctx.screen.use()
        self.ctx.disable(mgl.DEPTH_TEST)
        self.gui.render()
        self.ctx.disable(mgl.BLEND)
        self.ctx.enable(mgl.DEPTH_TEST)

    def process_window_resize(self, new_size):
        self.win_size = new_size
        self.game_gui.process_window_resize(new_size)
        # self.gizmos.process_window_resize(new_size)
        object_picker_m.ObjectPicker.process_window_resize(new_size)
