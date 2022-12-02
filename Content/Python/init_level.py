import unreal_engine as ue
from unreal_engine.classes import PyActor

# Create a new actor and add it to the level
actor = PyActor()
ue.add_actor_to_level(actor)

# Set the actor's location and rotation
actor.set_actor_location(ue.Vector(0, 0, 100))
actor.set_actor_rotation(ue.Rotator(0, 45, 0))
