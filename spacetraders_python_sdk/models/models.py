"""Models Schemas."""

from enum import Enum
from typing import Annotated, List, Optional

from pydantic import BaseModel, Field


class StatsSchema(BaseModel):
    """Stats Schema."""

    agents: Annotated[int, Field(description="Number of registered agents in the game.")]
    ships: Annotated[int, Field(description="Total number of ships in the game.")]
    systems: Annotated[int, Field(description="Total number of systems in the game.")]
    waypoints: Annotated[int, Field(description="Total number of waypoints in the game.")]


class MostCreditSchema(BaseModel):
    """Most Credit Schema."""

    agentSymbol: Annotated[str, Field(description="Symbol of the agent.")]
    credits: Annotated[int, Field(description="Amount of credits.", ge=-9007199254740991, le=9007199254740991)]


class MostSubmittedChartSchema(BaseModel):
    """Most Submitted Chart Schema."""

    agentSymbol: Annotated[str, Field(description="Symbol of the agent.")]
    chartCount: Annotated[int, Field(description="Amount of charts done by the agent.")]


class LeaderboardsSchema(BaseModel):
    """Leaderboards Schema."""

    mostCredits: Annotated[
        List[MostCreditSchema],
        Field(description="Top agents with the most credits."),
    ]
    mostSubmittedCharts: Annotated[
        List[MostSubmittedChartSchema],
        Field(description="Top agents with the most charted submitted."),
    ]


class ServerResetsSchema(BaseModel):
    """Server Resets Schema."""

    next: Annotated[str, Field(description="The date and time when the game server will reset.")]
    frequency: Annotated[str, Field(description="How often we intend to reset the game server.")]


class AnnouncementSchema(BaseModel):
    """Announcement Schema."""

    title: Annotated[str, Field(description="Title.")]
    body: Annotated[str, Field(description="Body.")]


class LinkSchema(BaseModel):
    """Link Schema."""

    name: Annotated[str, Field(description="Name.")]
    url: Annotated[str, Field(description="Url.")]


class StatusReponseSchema(BaseModel):
    """Status Reponse Schema."""

    status: Annotated[str, Field(description="The current status of the game server.")]
    version: Annotated[str, Field(description="The current version of the API.")]
    resetDate: Annotated[str, Field(description="The date when the game server was last reset.")]
    description: Annotated[str, Field(description="Description.")]
    stats: StatsSchema
    leaderboards: LeaderboardsSchema
    serverResets: ServerResetsSchema
    announcements: List[AnnouncementSchema]
    links: List[LinkSchema]


class MetaSchema(BaseModel):
    """Meta Schema."""

    total: Annotated[int, Field(description="Shows the total amount of items of this kind that exist.", ge=0)]
    page: Annotated[
        int,
        Field(
            description=(
                "A page denotes an amount of items, offset from the first item."
                "Each page holds an amount of items equal to the limit."
            ),
            ge=1,
            default=1,
        ),
    ] = 1
    limit: Annotated[
        int,
        Field(
            description="The amount of items in each page. Limits how many items can be fetched at once.",
            ge=1,
            le=20,
            default=10,
        ),
    ] = 10


# ---------------------------------------------------------
# AGENTS
# ---------------------------------------------------------
class AgentSchema(BaseModel):
    """Agent Schema."""

    accountId: Annotated[
        Optional[str],
        Field(
            description="Account ID that is tied to this agent. Only included on your own agent.",
            pattern="^[a-zA-Z0-9_-]+",
        ),
    ] = None
    symbol: Annotated[str, Field(description="Symbol of the agent.", pattern="^[a-zA-Z0-9_-]+$")]
    headquarters: Annotated[str, Field(description="The headquarters of the agent.", pattern="^[a-zA-Z0-9_-]+")]
    credits: Annotated[int, Field(description="Amount of credits.", ge=-9007199254740991, le=9007199254740991)]
    startingFaction: Annotated[str, Field(description="The faction the agent started with.", pattern="^[a-zA-Z0-9_-]+")]
    shipCount: Annotated[int, Field(description="How many ships are owned by the agent.")]


class AgentResponseSchema(BaseModel):
    """Agent Response Schema."""

    data: AgentSchema


class ListAgentsResponseSchema(BaseModel):
    """List Agents Response Schema."""

    data: List[AgentSchema]
    meta: MetaSchema


# ---------------------------------------------------------
# CONTRACTS
# ---------------------------------------------------------
class ContractTypeEnum(str, Enum):
    """Contract Type Enum."""

    PROCUREMENT = "PROCUREMENT"
    TRANSPORT = "TRANSPORT"
    SHUTTLE = "SHUTTLE"


class PaymentSchema(BaseModel):
    """Payment Schema."""

    onAccepted: Annotated[int, Field(description="The amount of credits received up front for accepting the contract.")]
    onFulfilled: Annotated[int, Field(description="The amount of credits received when the contract is fulfilled.")]


class DeliverSchema(BaseModel):
    """Deliver Schema."""

    tradeSymbol: Annotated[
        str, Field(description="The symbol of the trade good to deliver.", pattern="^[a-zA-Z0-9_-]+")
    ]
    destinationSymbol: Annotated[
        str, Field(description="The destination where goods need to be delivered.", pattern="^[a-zA-Z0-9_-]+")
    ]
    unitsRequired: Annotated[int, Field(description="The number of units that need to be delivered on this contract.")]
    unitsFulfilled: Annotated[int, Field(description="The number of units fulfilled on this contract.")]


class TermsSchema(BaseModel):
    """Terms Schema."""

    deadline: Annotated[str, Field(description="The deadline for the contract.")]
    payment: PaymentSchema
    deliver: List[DeliverSchema]


class ContractSchema(BaseModel):
    """Contract Schema."""

    id: Annotated[str, Field(description="ID of the contract.", pattern="^[a-zA-Z0-9_-]+")]
    factionSymbol: Annotated[str, Field(description="Symbol of the Contract.", pattern="^[a-zA-Z0-9_-]+$")]
    type: Annotated[ContractTypeEnum, Field(description="Type of contract.")]
    terms: Annotated[TermsSchema, Field(description="The terms to fulfill the contract.")]
    accepted: Annotated[
        bool, Field(description="Whether the contract has been accepted by the agent", default=False)
    ] = False
    fulfilled: Annotated[bool, Field(description="Whether the contract has been fulfilled", default=False)] = False
    deadlineToAccept: Annotated[
        str, Field(description="The time at which the contract is no longer available to be accepted.")
    ]


class ContractResponseSchema(BaseModel):
    """Contract Response Schema."""

    data: ContractSchema


class ListContractsResponseSchema(BaseModel):
    """List Contracts Response Schema."""

    data: List[ContractSchema]
    meta: MetaSchema


class AcceptContractSchema(BaseModel):
    """Accept Contract Schema."""

    agent: AgentSchema
    contract: ContractSchema


class AcceptContractResponseSchema(BaseModel):
    """Accept Contract Response Schema."""

    data: AcceptContractSchema


# ---------------------------------------------------------
# FACTIONS
# ---------------------------------------------------------
class FactionSymbolEnum(str, Enum):
    """Faction Symbol Enum."""

    COSMIC = "COSMIC"
    VOID = "VOID"
    GALACTIC = "GALACTIC"
    QUANTUM = "QUANTUM"
    DOMINION = "DOMINION"
    ASTRO = "ASTRO"
    CORSAIRS = "CORSAIRS"
    OBSIDIAN = "OBSIDIAN"
    AEGIS = "AEGIS"
    UNITED = "UNITED"
    SOLITARY = "SOLITARY"
    COBALT = "COBALT"
    OMEGA = "OMEGA"
    ECHO = "ECHO"
    LORDS = "LORDS"
    CULT = "CULT"
    ANCIENTS = "ANCIENTS"
    SHADOW = "SHADOW"
    ETHEREAL = "ETHEREAL"


class TraitSymbolEnum(str, Enum):
    """Trait Symbol Enum."""

    BUREAUCRATIC = "BUREAUCRATIC"
    SECRETIVE = "SECRETIVE"
    CAPITALISTIC = "CAPITALISTIC"
    INDUSTRIOUS = "INDUSTRIOUS"
    PEACEFUL = "PEACEFUL"
    DISTRUSTFUL = "DISTRUSTFUL"
    WELCOMING = "WELCOMING"
    SMUGGLERS = "SMUGGLERS"
    SCAVENGERS = "SCAVENGERS"
    REBELLIOUS = "REBELLIOUS"
    EXILES = "EXILES"
    PIRATES = "PIRATES"
    RAIDERS = "RAIDERS"
    CLAN = "CLAN"
    GUILD = "GUILD"
    DOMINION = "DOMINION"
    FRINGE = "FRINGE"
    FORSAKEN = "FORSAKEN"
    ISOLATED = "ISOLATED"
    LOCALIZED = "LOCALIZED"
    ESTABLISHED = "ESTABLISHED"
    NOTABLE = "NOTABLE"
    DOMINANT = "DOMINANT"
    INESCAPABLE = "INESCAPABLE"
    INNOVATIVE = "INNOVATIVE"
    BOLD = "BOLD"
    VISIONARY = "VISIONARY"
    CURIOUS = "CURIOUS"
    DARING = "DARING"
    EXPLORATORY = "EXPLORATORY"
    RESOURCEFUL = "RESOURCEFUL"
    FLEXIBLE = "FLEXIBLE"
    COOPERATIVE = "COOPERATIVE"
    UNITED = "UNITED"
    STRATEGIC = "STRATEGIC"
    INTELLIGENT = "INTELLIGENT"
    RESEARCH_FOCUSED = "RESEARCH_FOCUSED"
    COLLABORATIVE = "COLLABORATIVE"
    PROGRESSIVE = "PROGRESSIVE"
    MILITARISTIC = "MILITARISTIC"
    TECHNOLOGICALLY_ADVANCED = "TECHNOLOGICALLY_ADVANCED"
    AGGRESSIVE = "AGGRESSIVE"
    IMPERIALISTIC = "IMPERIALISTIC"
    TREASURE_HUNTERS = "TREASURE_HUNTERS"
    DEXTEROUS = "DEXTEROUS"
    UNPREDICTABLE = "UNPREDICTABLE"
    BRUTAL = "BRUTAL"
    FLEETING = "FLEETING"
    ADAPTABLE = "ADAPTABLE"
    SELF_SUFFICIENT = "SELF_SUFFICIENT"
    DEFENSIVE = "DEFENSIVE"
    PROUD = "PROUD"
    DIVERSE = "DIVERSE"
    INDEPENDENT = "INDEPENDENT"
    SELF_INTERESTED = "SELF_INTERESTED"
    FRAGMENTED = "FRAGMENTED"
    COMMERCIAL = "COMMERCIAL"
    FREE_MARKETS = "FREE_MARKETS"
    ENTREPRENEURIAL = "ENTREPRENEURIAL"


class TraitSchema(BaseModel):
    """Trait Schema."""

    symbol: Annotated[TraitSymbolEnum, Field(description="The unique identifier of the trait.")]
    name: Annotated[str, Field(description="The name of the trait.")]
    description: Annotated[str, Field(description="A description of the trait.")]


class FactionSchema(BaseModel):
    """Faction Schema."""

    symbol: Annotated[FactionSymbolEnum, Field(description="The symbol of the faction.")]
    name: Annotated[str, Field(description="Name of the faction.")]
    description: Annotated[str, Field(description="Description of the faction.")]
    headquarters: Annotated[str, Field(description="The waypoint in which the faction's HQ is located in.")]
    traits: Annotated[List[TraitSchema], Field(description="List of traits that define this faction.")]
    isRecruiting: Annotated[bool, Field(description="Whether or not the faction is currently recruiting new agents.")]


class FactionResponseSchema(BaseModel):
    """Faction Response Schema."""

    data: FactionSchema


class ListFactionsResponseSchema(BaseModel):
    """List Factions Response Schema."""

    data: List[FactionSchema]
    meta: MetaSchema


# ---------------------------------------------------------
# WAYPOINTS
# ---------------------------------------------------------
class WaypointTypeEnum(str, Enum):
    """Waypoint Type Enum."""

    PLANET = "PLANET"
    GAS_GIANT = "GAS_GIANT"
    MOON = "MOON"
    ORBITAL_STATION = "ORBITAL_STATION"
    JUMP_GATE = "JUMP_GATE"
    ASTEROID_FIELD = "ASTEROID_FIELD"
    ASTEROID = "ASTEROID"
    ENGINEERED_ASTEROID = "ENGINEERED_ASTEROID"
    ASTEROID_BASE = "ASTEROID_BASE"
    NEBULA = "NEBULA"
    DEBRIS_FIELD = "DEBRIS_FIELD"
    GRAVITY_WELL = "GRAVITY_WELL"
    ARTIFICIAL_GRAVITY_WELL = "ARTIFICIAL_GRAVITY_WELL"
    FUEL_STATION = "FUEL_STATION"


class WaypointOrbitalSchema(BaseModel):
    """Waypoint Orbital Schema."""

    symbol: Annotated[str, Field(description="The symbol of the orbiting waypoint.")]


class WaypointFactionSchema(BaseModel):
    """Waypoint Faction Schema."""

    symbol: Annotated[FactionSymbolEnum, Field(description="The symbol of the faction.")]


class WaypointTraitSymbolEnum(str, Enum):
    """Waypoint Trait Symbol Enum."""

    UNCHARTED = "UNCHARTED"
    UNDER_CONSTRUCTION = "UNDER_CONSTRUCTION"
    MARKETPLACE = "MARKETPLACE"
    SHIPYARD = "SHIPYARD"
    OUTPOST = "OUTPOST"
    SCATTERED_SETTLEMENTS = "SCATTERED_SETTLEMENTS"
    SPRAWLING_CITIES = "SPRAWLING_CITIES"
    MEGA_STRUCTURES = "MEGA_STRUCTURES"
    PIRATE_BASE = "PIRATE_BASE"
    OVERCROWDED = "OVERCROWDED"
    HIGH_TECH = "HIGH_TECH"
    CORRUPT = "CORRUPT"
    BUREAUCRATIC = "BUREAUCRATIC"
    TRADING_HUB = "TRADING_HUB"
    INDUSTRIAL = "INDUSTRIAL"
    BLACK_MARKET = "BLACK_MARKET"
    RESEARCH_FACILITY = "RESEARCH_FACILITY"
    MILITARY_BASE = "MILITARY_BASE"
    SURVEILLANCE_OUTPOST = "SURVEILLANCE_OUTPOST"
    EXPLORATION_OUTPOST = "EXPLORATION_OUTPOST"
    MINERAL_DEPOSITS = "MINERAL_DEPOSITS"
    COMMON_METAL_DEPOSITS = "COMMON_METAL_DEPOSITS"
    PRECIOUS_METAL_DEPOSITS = "PRECIOUS_METAL_DEPOSITS"
    RARE_METAL_DEPOSITS = "RARE_METAL_DEPOSITS"
    METHANE_POOLS = "METHANE_POOLS"
    ICE_CRYSTALS = "ICE_CRYSTALS"
    EXPLOSIVE_GASES = "EXPLOSIVE_GASES"
    STRONG_MAGNETOSPHERE = "STRONG_MAGNETOSPHERE"
    VIBRANT_AURORAS = "VIBRANT_AURORAS"
    SALT_FLATS = "SALT_FLATS"
    CANYONS = "CANYONS"
    PERPETUAL_DAYLIGHT = "PERPETUAL_DAYLIGHT"
    PERPETUAL_OVERCAST = "PERPETUAL_OVERCAST"
    DRY_SEABEDS = "DRY_SEABEDS"
    MAGMA_SEAS = "MAGMA_SEAS"
    SUPERVOLCANOES = "SUPERVOLCANOES"
    ASH_CLOUDS = "ASH_CLOUDS"
    VAST_RUINS = "VAST_RUINS"
    MUTATED_FLORA = "MUTATED_FLORA"
    TERRAFORMED = "TERRAFORMED"
    EXTREME_TEMPERATURES = "EXTREME_TEMPERATURES"
    EXTREME_PRESSURE = "EXTREME_PRESSURE"
    DIVERSE_LIFE = "DIVERSE_LIFE"
    SCARCE_LIFE = "SCARCE_LIFE"
    FOSSILS = "FOSSILS"
    WEAK_GRAVITY = "WEAK_GRAVITY"
    STRONG_GRAVITY = "STRONG_GRAVITY"
    CRUSHING_GRAVITY = "CRUSHING_GRAVITY"
    TOXIC_ATMOSPHERE = "TOXIC_ATMOSPHERE"
    CORROSIVE_ATMOSPHERE = "CORROSIVE_ATMOSPHERE"
    BREATHABLE_ATMOSPHERE = "BREATHABLE_ATMOSPHERE"
    THIN_ATMOSPHERE = "THIN_ATMOSPHERE"
    JOVIAN = "JOVIAN"
    ROCKY = "ROCKY"
    VOLCANIC = "VOLCANIC"
    FROZEN = "FROZEN"
    SWAMP = "SWAMP"
    BARREN = "BARREN"
    TEMPERATE = "TEMPERATE"
    JUNGLE = "JUNGLE"
    OCEAN = "OCEAN"
    RADIOACTIVE = "RADIOACTIVE"
    MICRO_GRAVITY_ANOMALIES = "MICRO_GRAVITY_ANOMALIES"
    DEBRIS_CLUSTER = "DEBRIS_CLUSTER"
    DEEP_CRATERS = "DEEP_CRATERS"
    SHALLOW_CRATERS = "SHALLOW_CRATERS"
    UNSTABLE_COMPOSITION = "UNSTABLE_COMPOSITION"
    HOLLOWED_INTERIOR = "HOLLOWED_INTERIOR"
    STRIPPED = "STRIPPED"


class WaypointTraitSchema(BaseModel):
    """Waypoint Trait Schema."""

    symbol: Annotated[WaypointTraitSymbolEnum, Field(description="The unique identifier of the trait.")]
    name: Annotated[str, Field(description="The name of the trait.")]
    description: Annotated[str, Field(description="A description of the trait.")]


class WaypointModifierSymbolEnum(str, Enum):
    """Waypont Modifier Symbol Enum."""

    STRIPPED = "STRIPPED"
    UNSTABLE = "UNSTABLE"
    RADIATION_LEAK = "RADIATION_LEAK"
    CRITICAL_LIMIT = "CRITICAL_LIMIT"
    CIVIL_UNREST = "CIVIL_UNREST"


class WaypointModifierSchema(BaseModel):
    """Waypont Modifier Schema."""

    symbol: Annotated[WaypointModifierSymbolEnum, Field(description="The unique identifier of the modifier.")]
    name: Annotated[str, Field(description="The name of the trait.")]
    description: Annotated[str, Field(description="A description of the trait.")]


class ChartSchema(BaseModel):
    """Chart Schema."""

    waypointSymbol: Annotated[Optional[str], Field(description="The symbol of the waypoint.")] = None
    submittedBy: Annotated[str, Field(description="The agent that submitted the chart for this waypoint.")]
    submittedOn: Annotated[str, Field(description="The time the chart for this waypoint was submitted.")]


class WaypointSchema(BaseModel):
    """Waypoint Schema."""

    symbol: Annotated[str, Field(description="The symbol of the waypoint.")]
    type: Annotated[WaypointTypeEnum, Field(description="The type of waypoint.")]
    x: Annotated[
        int,
        Field(
            description=(
                "Relative position of the waypoint on the system's x axis."
                "This is not an absolute position in the universe."
            )
        ),
    ]
    y: Annotated[
        int,
        Field(
            description=(
                "Relative position of the waypoint on the system's y axis."
                "This is not an absolute position in the universe."
            )
        ),
    ]
    orbitals: Annotated[List[WaypointOrbitalSchema], Field(description="Waypoints that orbit this waypoint.")]
    orbits: Annotated[
        Optional[str],
        Field(
            description=(
                "The symbol of the parent waypoint, if this waypoint is in orbit around another waypoint."
                "Otherwise this value is undefined."
            )
        ),
    ] = None
    faction: Annotated[
        Optional[WaypointFactionSchema], Field(description="The faction that controls the waypoint.")
    ] = None
    traits: Annotated[List[WaypointTraitSchema], Field(description="The traits of the waypoint.")]
    modifiers: Annotated[List[WaypointModifierSchema], Field(description="The modifiers of the waypoint.")]
    chart: Annotated[
        Optional[ChartSchema],
        Field(description="The chart of a system or waypoint, which makes the location visible to other agents."),
    ] = None
    isUnderConstruction: Annotated[bool, Field(description="True if the waypoint is under construction.")]


class ListWaypointsResponseSchema(BaseModel):
    """List Systems Response Schema."""

    data: List[WaypointSchema]
    meta: MetaSchema


class WaypointResponseSchema(BaseModel):
    """System Response Schema."""

    data: WaypointSchema


# ---------------------------------------------------------
# SYSTEMS
# ---------------------------------------------------------
class SystemTypeEnum(str, Enum):
    """System Type Enum."""

    NEUTRON_STAR = "NEUTRON_STAR"
    RED_STAR = "RED_STAR"
    ORANGE_STAR = "ORANGE_STAR"
    BLUE_STAR = "BLUE_STAR"
    YOUNG_STAR = "YOUNG_STAR"
    WHITE_DWARF = "WHITE_DWARF"
    BLACK_HOLE = "BLACK_HOLE"
    HYPERGIANT = "HYPERGIANT"
    NEBULA = "NEBULA"
    UNSTABLE = "UNSTABLE"


class SystemWaypointSchema(BaseModel):
    """Waypoint Schema."""

    symbol: Annotated[str, Field(description="The symbol of the waypoint.")]
    type: Annotated[WaypointTypeEnum, Field(description="The type of waypoint.")]
    x: Annotated[
        int,
        Field(
            description=(
                "Relative position of the waypoint on the system's x axis."
                "This is not an absolute position in the universe."
            )
        ),
    ]
    y: Annotated[
        int,
        Field(
            description=(
                "Relative position of the waypoint on the system's y axis."
                "This is not an absolute position in the universe."
            )
        ),
    ]
    orbitals: Annotated[List[WaypointOrbitalSchema], Field(description="Waypoints that orbit this waypoint.")]
    orbits: Annotated[
        Optional[str],
        Field(
            description=(
                "The symbol of the parent waypoint, if this waypoint is in orbit around another waypoint."
                "Otherwise this value is undefined."
            )
        ),
    ] = None


class SystemSchema(BaseModel):
    """System Schema."""

    symbol: Annotated[str, Field(description="The symbol of the system.")]
    sectorSymbol: Annotated[str, Field(description="The symbol of the system.")]
    type: Annotated[SystemTypeEnum, Field(description="The type of system.")]
    x: Annotated[int, Field(description="Relative position of the system in the sector in the x axis.")]
    y: Annotated[int, Field(description="Relative position of the system in the sector in the y axis.")]
    waypoints: Annotated[List[SystemWaypointSchema], Field(description="Waypoints in this system.")]
    factions: Annotated[List[WaypointFactionSchema], Field(description="Factions that control this system.")]


class SystemResponseSchema(BaseModel):
    """System Response Schema."""

    data: SystemSchema


class ListSystemsResponseSchema(BaseModel):
    """List Systems Response Schema."""

    data: List[SystemSchema]
    meta: MetaSchema


# ---------------------------------------------------------
# MARKETPLACE
# ---------------------------------------------------------
class TradeSymbolEnum(str, Enum):
    """Good Symbol Enum."""

    PRECIOUS_STONES = "PRECIOUS_STONES"
    QUARTZ_SAND = "QUARTZ_SAND"
    SILICON_CRYSTALS = "SILICON_CRYSTALS"
    AMMONIA_ICE = "AMMONIA_ICE"
    LIQUID_HYDROGEN = "LIQUID_HYDROGEN"
    LIQUID_NITROGEN = "LIQUID_NITROGEN"
    ICE_WATER = "ICE_WATER"
    EXOTIC_MATTER = "EXOTIC_MATTER"
    ADVANCED_CIRCUITRY = "ADVANCED_CIRCUITRY"
    GRAVITON_EMITTERS = "GRAVITON_EMITTERS"
    IRON = "IRON"
    IRON_ORE = "IRON_ORE"
    COPPER = "COPPER"
    COPPER_ORE = "COPPER_ORE"
    ALUMINUM = "ALUMINUM"
    ALUMINUM_ORE = "ALUMINUM_ORE"
    SILVER = "SILVER"
    SILVER_ORE = "SILVER_ORE"
    GOLD = "GOLD"
    GOLD_ORE = "GOLD_ORE"
    PLATINUM = "PLATINUM"
    PLATINUM_ORE = "PLATINUM_ORE"
    DIAMONDS = "DIAMONDS"
    URANITE = "URANITE"
    URANITE_ORE = "URANITE_ORE"
    MERITIUM = "MERITIUM"
    MERITIUM_ORE = "MERITIUM_ORE"
    HYDROCARBON = "HYDROCARBON"
    ANTIMATTER = "ANTIMATTER"
    FAB_MATS = "FAB_MATS"
    FERTILIZERS = "FERTILIZERS"
    FABRICS = "FABRICS"
    FOOD = "FOOD"
    JEWELRY = "JEWELRY"
    MACHINERY = "MACHINERY"
    FIREARMS = "FIREARMS"
    ASSAULT_RIFLES = "ASSAULT_RIFLES"
    MILITARY_EQUIPMENT = "MILITARY_EQUIPMENT"
    EXPLOSIVES = "EXPLOSIVES"
    LAB_INSTRUMENTS = "LAB_INSTRUMENTS"
    AMMUNITION = "AMMUNITION"
    ELECTRONICS = "ELECTRONICS"
    SHIP_PLATING = "SHIP_PLATING"
    SHIP_PARTS = "SHIP_PARTS"
    EQUIPMENT = "EQUIPMENT"
    FUEL = "FUEL"
    MEDICINE = "MEDICINE"
    DRUGS = "DRUGS"
    CLOTHING = "CLOTHING"
    MICROPROCESSORS = "MICROPROCESSORS"
    PLASTICS = "PLASTICS"
    POLYNUCLEOTIDES = "POLYNUCLEOTIDES"
    BIOCOMPOSITES = "BIOCOMPOSITES"
    QUANTUM_STABILIZERS = "QUANTUM_STABILIZERS"
    NANOBOTS = "NANOBOTS"
    AI_MAINFRAMES = "AI_MAINFRAMES"
    QUANTUM_DRIVES = "QUANTUM_DRIVES"
    ROBOTIC_DRONES = "ROBOTIC_DRONES"
    CYBER_IMPLANTS = "CYBER_IMPLANTS"
    GENE_THERAPEUTICS = "GENE_THERAPEUTICS"
    NEURAL_CHIPS = "NEURAL_CHIPS"
    MOOD_REGULATORS = "MOOD_REGULATORS"
    VIRAL_AGENTS = "VIRAL_AGENTS"
    MICRO_FUSION_GENERATORS = "MICRO_FUSION_GENERATORS"
    SUPERGRAINS = "SUPERGRAINS"
    LASER_RIFLES = "LASER_RIFLES"
    HOLOGRAPHICS = "HOLOGRAPHICS"
    SHIP_SALVAGE = "SHIP_SALVAGE"
    RELIC_TECH = "RELIC_TECH"
    NOVEL_LIFEFORMS = "NOVEL_LIFEFORMS"
    BOTANICAL_SPECIMENS = "BOTANICAL_SPECIMENS"
    CULTURAL_ARTIFACTS = "CULTURAL_ARTIFACTS"
    FRAME_PROBE = "FRAME_PROBE"
    FRAME_DRONE = "FRAME_DRONE"
    FRAME_INTERCEPTOR = "FRAME_INTERCEPTOR"
    FRAME_RACER = "FRAME_RACER"
    FRAME_FIGHTER = "FRAME_FIGHTER"
    FRAME_FRIGATE = "FRAME_FRIGATE"
    FRAME_SHUTTLE = "FRAME_SHUTTLE"
    FRAME_EXPLORER = "FRAME_EXPLORER"
    FRAME_MINER = "FRAME_MINER"
    FRAME_LIGHT_FREIGHTER = "FRAME_LIGHT_FREIGHTER"
    FRAME_HEAVY_FREIGHTER = "FRAME_HEAVY_FREIGHTER"
    FRAME_TRANSPORT = "FRAME_TRANSPORT"
    FRAME_DESTROYER = "FRAME_DESTROYER"
    FRAME_CRUISER = "FRAME_CRUISER"
    FRAME_CARRIER = "FRAME_CARRIER"
    REACTOR_SOLAR_I = "REACTOR_SOLAR_I"
    REACTOR_FUSION_I = "REACTOR_FUSION_I"
    REACTOR_FISSION_I = "REACTOR_FISSION_I"
    REACTOR_CHEMICAL_I = "REACTOR_CHEMICAL_I"
    REACTOR_ANTIMATTER_I = "REACTOR_ANTIMATTER_I"
    ENGINE_IMPULSE_DRIVE_I = "ENGINE_IMPULSE_DRIVE_I"
    ENGINE_ION_DRIVE_I = "ENGINE_ION_DRIVE_I"
    ENGINE_ION_DRIVE_II = "ENGINE_ION_DRIVE_II"
    ENGINE_HYPER_DRIVE_I = "ENGINE_HYPER_DRIVE_I"
    MODULE_MINERAL_PROCESSOR_I = "MODULE_MINERAL_PROCESSOR_I"
    MODULE_GAS_PROCESSOR_I = "MODULE_GAS_PROCESSOR_I"
    MODULE_CARGO_HOLD_I = "MODULE_CARGO_HOLD_I"
    MODULE_CARGO_HOLD_II = "MODULE_CARGO_HOLD_II"
    MODULE_CARGO_HOLD_III = "MODULE_CARGO_HOLD_III"
    MODULE_CREW_QUARTERS_I = "MODULE_CREW_QUARTERS_I"
    MODULE_ENVOY_QUARTERS_I = "MODULE_ENVOY_QUARTERS_I"
    MODULE_PASSENGER_CABIN_I = "MODULE_PASSENGER_CABIN_I"
    MODULE_MICRO_REFINERY_I = "MODULE_MICRO_REFINERY_I"
    MODULE_SCIENCE_LAB_I = "MODULE_SCIENCE_LAB_I"
    MODULE_JUMP_DRIVE_I = "MODULE_JUMP_DRIVE_I"
    MODULE_JUMP_DRIVE_II = "MODULE_JUMP_DRIVE_II"
    MODULE_JUMP_DRIVE_III = "MODULE_JUMP_DRIVE_III"
    MODULE_WARP_DRIVE_I = "MODULE_WARP_DRIVE_I"
    MODULE_WARP_DRIVE_II = "MODULE_WARP_DRIVE_II"
    MODULE_WARP_DRIVE_III = "MODULE_WARP_DRIVE_III"
    MODULE_SHIELD_GENERATOR_I = "MODULE_SHIELD_GENERATOR_I"
    MODULE_SHIELD_GENERATOR_II = "MODULE_SHIELD_GENERATOR_II"
    MODULE_ORE_REFINERY_I = "MODULE_ORE_REFINERY_I"
    MODULE_FUEL_REFINERY_I = "MODULE_FUEL_REFINERY_I"
    MOUNT_GAS_SIPHON_I = "MOUNT_GAS_SIPHON_I"
    MOUNT_GAS_SIPHON_II = "MOUNT_GAS_SIPHON_II"
    MOUNT_GAS_SIPHON_III = "MOUNT_GAS_SIPHON_III"
    MOUNT_SURVEYOR_I = "MOUNT_SURVEYOR_I"
    MOUNT_SURVEYOR_II = "MOUNT_SURVEYOR_II"
    MOUNT_SURVEYOR_III = "MOUNT_SURVEYOR_III"
    MOUNT_SENSOR_ARRAY_I = "MOUNT_SENSOR_ARRAY_I"
    MOUNT_SENSOR_ARRAY_II = "MOUNT_SENSOR_ARRAY_II"
    MOUNT_SENSOR_ARRAY_III = "MOUNT_SENSOR_ARRAY_III"
    MOUNT_MINING_LASER_I = "MOUNT_MINING_LASER_I"
    MOUNT_MINING_LASER_II = "MOUNT_MINING_LASER_II"
    MOUNT_MINING_LASER_III = "MOUNT_MINING_LASER_III"
    MOUNT_LASER_CANNON_I = "MOUNT_LASER_CANNON_I"
    MOUNT_MISSILE_LAUNCHER_I = "MOUNT_MISSILE_LAUNCHER_I"
    MOUNT_TURRET_I = "MOUNT_TURRET_I"
    SHIP_PROBE = "SHIP_PROBE"
    SHIP_MINING_DRONE = "SHIP_MINING_DRONE"
    SHIP_SIPHON_DRONE = "SHIP_SIPHON_DRONE"
    SHIP_INTERCEPTOR = "SHIP_INTERCEPTOR"
    SHIP_LIGHT_HAULER = "SHIP_LIGHT_HAULER"
    SHIP_COMMAND_FRIGATE = "SHIP_COMMAND_FRIGATE"
    SHIP_EXPLORER = "SHIP_EXPLORER"
    SHIP_HEAVY_FREIGHTER = "SHIP_HEAVY_FREIGHTER"
    SHIP_LIGHT_SHUTTLE = "SHIP_LIGHT_SHUTTLE"
    SHIP_ORE_HOUND = "SHIP_ORE_HOUND"
    SHIP_REFINING_FREIGHTER = "SHIP_REFINING_FREIGHTER"
    SHIP_SURVEYOR = "SHIP_SURVEYOR"


class TradeGoodSchema(BaseModel):
    """Export Schema."""

    symbol: Annotated[
        TradeSymbolEnum,
        Field(
            description="The symbol of the market. The symbol is the same as the waypoint where the market is located."
        ),
    ]
    name: Annotated[str, Field(description="The name of the good.")]
    description: Annotated[str, Field(description="A description of the good.")]


class TransactionTypeEnum(str, Enum):
    """Transaction Type Enum."""

    PURCHASE = "PURCHASE"
    SELL = "SELL"


class TransactionSchema(BaseModel):
    """Transaction Schema."""

    waypointSymbol: Annotated[str, Field(description="The symbol of the waypoint.")]
    shipSymbol: Annotated[str, Field(description="The symbol of the ship that made the transaction.")]
    tradeSymbol: Annotated[str, Field(description="The symbol of the trade good.")]
    transactionType: Annotated[TransactionTypeEnum, Field(description="The type of transaction.", alias="type")]
    units: Annotated[int, Field(description="The number of units of the transaction.", ge=0)]
    pricePerUnit: Annotated[int, Field(description="The price per unit of the transaction.", ge=0)]

    totalPrice: Annotated[int, Field(description="The total price of the transaction.", ge=0)]
    timestamp: Annotated[str, Field(description="The timestamp of the transaction.")]


class MarketTradeGoodTypeEnum(str, Enum):
    """Market Trade Good Type Enum."""

    EXPORT = "EXPORT"
    IMPORT = "IMPORT"
    EXCHANGE = "EXCHANGE"


class SupplyEnum(str, Enum):
    """Market Trade Good Type Enum."""

    SCARCE = "SCARCE"
    LIMITED = "LIMITED"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    ABUNDANT = "ABUNDANT"


class ActivityeEnum(str, Enum):
    """Market Trade Good Type Enum."""

    WEAK = "WEAK"
    GROWING = "GROWING"
    STRONG = "STRONG"
    RESTRICTED = "RESTRICTED"


class MarketTradeGoodSchema(BaseModel):
    """Market Trade Good Schema."""

    symbol: Annotated[TradeSymbolEnum, Field(description="The good's symbol.")]
    type: Annotated[MarketTradeGoodTypeEnum, Field(description="The type of trade good (export, import, or exchange).")]
    tradeVolume: Annotated[
        int,
        Field(
            description=(
                "This is the maximum number of units that can be purchased or sold at this market "
                "in a single trade for this good."
                "Trade volume also gives an indication of price volatility."
                "A market with a low trade volume will have large price swings, "
                "while high trade volume will be more resilient to price changes."
            )
        ),
    ]
    supply: Annotated[SupplyEnum, Field(description="The supply level of a trade good.")]
    activity: Annotated[
        ActivityeEnum,
        Field(
            description=(
                "The activity level of a trade good."
                "If the good is an import, this represents how strong consumption is."
                "If the good is an export, this represents how strong the production is for the good."
                "When activity is strong, consumption or production is near maximum capacity."
                "When activity is weak, consumption or production is near minimum capacity."
            )
        ),
    ]
    purchasePrice: Annotated[int, Field(description="The price at which this good can be purchased from the market.")]
    sellPrice: Annotated[int, Field(description="The price at which this good can be sold to the market.")]


class MarketSchema(BaseModel):
    """Market Schema."""

    symbol: Annotated[
        str,
        Field(
            description="The symbol of the market. The symbol is the same as the waypoint where the market is located."
        ),
    ]
    exports: Annotated[
        List[TradeGoodSchema], Field(description="The list of goods that are exported from this market.")
    ]
    imports: Annotated[
        List[TradeGoodSchema], Field(description="The list of goods that are sought as imports in this market.")
    ]
    exchange: Annotated[
        List[TradeGoodSchema],
        Field(description="The list of goods that are bought and sold between agents at this market."),
    ]
    transactions: Annotated[
        List[TransactionSchema],
        Field(
            description=(
                "The list of recent transactions at this market. Visible only when a ship is present at the market."
            )
        ),
    ]
    tradeGoods: Annotated[
        List[MarketTradeGoodSchema],
        Field(
            description=(
                "The list of goods that are traded at this market. Visible only when a ship is present at the market."
            )
        ),
    ]


class MarketResponseSchema(BaseModel):
    """Market Response Schema."""

    data: MarketSchema


class MarketTranscationTypeEnum(str, Enum):
    """Market Transcation Type Enum."""

    PURCHASE = "PURCHASE"
    SELL = "SELL"


class MarketTranscationSchema(BaseModel):
    """Market Transaction Schema."""

    waypointSymbol: Annotated[str, Field(description="The symbol of the waypoint.")]
    shipSymbol: Annotated[str, Field(description="The symbol of the ship that made the transaction.")]
    tradeSymbol: Annotated[str, Field(description="The symbol of the trade good..")]
    type: Annotated[MarketTranscationTypeEnum, Field(description="The type of transaction.")]
    units: Annotated[int, Field(description="The number of units of the transaction.", ge=0)]
    pricePerUnit: Annotated[int, Field(description="The price per unit of the transaction.", ge=0)]
    totalPrice: Annotated[int, Field(description="The total price of the transaction.", ge=0)]
    timestamp: Annotated[str, Field(description="The timestamp of the transaction.")]


# ---------------------------------------------------------
# SHIPS
# ---------------------------------------------------------
class ShipTypeEnum(str, Enum):
    """Ship Type Enum."""

    SHIP_PROBE = "SHIP_PROBE"
    SHIP_MINING_DRONE = "SHIP_MINING_DRONE"
    SHIP_SIPHON_DRONE = "SHIP_SIPHON_DRONE"
    SHIP_INTERCEPTOR = "SHIP_INTERCEPTOR"
    SHIP_LIGHT_HAULER = "SHIP_LIGHT_HAULER"
    SHIP_COMMAND_FRIGATE = "SHIP_COMMAND_FRIGATE"
    SHIP_EXPLORER = "SHIP_EXPLORER"
    SHIP_HEAVY_FREIGHTER = "SHIP_HEAVY_FREIGHTER"
    SHIP_LIGHT_SHUTTLE = "SHIP_LIGHT_SHUTTLE"
    SHIP_ORE_HOUND = "SHIP_ORE_HOUND"
    SHIP_REFINING_FREIGHTER = "SHIP_REFINING_FREIGHTER"
    SHIP_SURVEYOR = "SHIP_SURVEYOR"


class ShipTypeSchema(BaseModel):
    """Ship Type Schema."""

    type: Annotated[ShipTypeEnum, Field(description="Type of ship")]


class ShipRequirementSchema(BaseModel):
    """Ship Requirement Schema."""

    power: Annotated[int, Field(description="The amount of power required from the reactor.", default=0)] = 0
    crew: Annotated[
        int,
        Field(description="The number of crew required for operation.", default=0),
    ] = 0
    slots: Annotated[
        int,
        Field(description="The number of module slots required for installation.", default=0),
    ] = 0


class ShipFrameSymbolEnum(str, Enum):
    """Ship Frame Symbol Enum."""

    FRAME_PROBE = "FRAME_PROBE"
    FRAME_DRONE = "FRAME_DRONE"
    FRAME_INTERCEPTOR = "FRAME_INTERCEPTOR"
    FRAME_RACER = "FRAME_RACER"
    FRAME_FIGHTER = "FRAME_FIGHTER"
    FRAME_FRIGATE = "FRAME_FRIGATE"
    FRAME_SHUTTLE = "FRAME_SHUTTLE"
    FRAME_EXPLORER = "FRAME_EXPLORER"
    FRAME_MINER = "FRAME_MINER"
    FRAME_LIGHT_FREIGHTER = "FRAME_LIGHT_FREIGHTER"
    FRAME_HEAVY_FREIGHTER = "FRAME_HEAVY_FREIGHTER"
    FRAME_TRANSPORT = "FRAME_TRANSPORT"
    FRAME_DESTROYER = "FRAME_DESTROYER"
    FRAME_CRUISER = "FRAME_CRUISER"
    FRAME_CARRIER = "FRAME_CARRIER"


class ShipFrameSchema(BaseModel):
    """Ship Frame Schema."""

    symbol: Annotated[ShipFrameSymbolEnum, Field(description="Symbol of the frame.")]
    name: Annotated[str, Field(description="Name of the frame.")]
    description: Annotated[str, Field(description="Description of the frame.")]
    condition: Annotated[
        float,
        Field(
            description=(
                "The repairable condition of a component."
                "A value of 0 indicates the component needs significant repairs, "
                "while a value of 1 indicates the component is in near perfect condition."
                "As the condition of a component is repaired, the overall integrity of the component decreases."
            ),
            ge=0,
            le=1,
        ),
    ]
    integrity: Annotated[
        float,
        Field(
            description=(
                "The overall integrity of the component, which determines the performance of the component."
                "A value of 0 indicates that the component is almost completely degraded, "
                "while a value of 1 indicates that the component is in near perfect condition."
                "The integrity of the component is non-repairable, and represents permanent wear over time."
            ),
            ge=0,
            le=1,
        ),
    ]
    moduleSlots: Annotated[
        int,
        Field(
            description=(
                "The amount of slots that can be dedicated to modules installed in the ship."
                "Each installed module take up a number of slots, and once there are no more slots, "
                "no new modules can be installed."
            ),
            ge=0,
        ),
    ]
    mountingPoints: Annotated[
        int,
        Field(
            description=(
                "The amount of slots that can be dedicated to mounts installed in the ship."
                "Each installed mount takes up a number of points, and once there are no more points remaining, "
                "no new mounts can be installed."
            ),
            ge=0,
        ),
    ]
    fuelCapacity: Annotated[
        int,
        Field(
            description=(
                "The maximum amount of fuel that can be stored in this ship."
                "When refueling, the ship will be refueled to this amount."
            ),
            ge=0,
        ),
    ]
    requirements: Annotated[ShipRequirementSchema, Field(description="The requirements for installation on a ship")]


class ShipReactorSymbolEnum(str, Enum):
    """Ship Reactor Symbol Enum."""

    REACTOR_SOLAR_I = "REACTOR_SOLAR_I"
    REACTOR_FUSION_I = "REACTOR_FUSION_I"
    REACTOR_FISSION_I = "REACTOR_FISSION_I"
    REACTOR_CHEMICAL_I = "REACTOR_CHEMICAL_I"
    REACTOR_ANTIMATTER_I = "REACTOR_ANTIMATTER_I"


class ShipReactorSchema(BaseModel):
    """Ship Reactor Schema."""

    symbol: Annotated[ShipReactorSymbolEnum, Field(description="Symbol of the reactor.")]
    name: Annotated[str, Field(description="Name of the reactor.")]
    description: Annotated[str, Field(description="Description of the reactor.")]
    condition: Annotated[
        float,
        Field(
            description=(
                "The repairable condition of a component."
                "A value of 0 indicates the component needs significant repairs, "
                "while a value of 1 indicates the component is in near perfect condition."
                "As the condition of a component is repaired, the overall integrity of the component decreases."
            ),
            ge=0,
            le=1,
        ),
    ]
    integrity: Annotated[
        float,
        Field(
            description=(
                "The overall integrity of the component, which determines the performance of the component."
                "A value of 0 indicates that the component is almost completely degraded, "
                "while a value of 1 indicates that the component is in near perfect condition."
                "The integrity of the component is non-repairable, and represents permanent wear over time."
            ),
            ge=0,
            le=1,
        ),
    ]
    powerOutput: Annotated[
        int,
        Field(
            description=(
                "The amount of power provided by this reactor."
                "The more power a reactor provides to the ship, "
                "the lower the cooldown it gets when using a module or mount that taxes the ship's power."
            ),
            ge=1,
        ),
    ]
    requirements: Annotated[ShipRequirementSchema, Field(description="The requirements for installation on a ship")]


class ShipEngineSymbolEnum(str, Enum):
    """Ship Engine Symbol Enum."""

    ENGINE_IMPULSE_DRIVE_I = "ENGINE_IMPULSE_DRIVE_I"
    ENGINE_ION_DRIVE_I = "ENGINE_ION_DRIVE_I"
    ENGINE_ION_DRIVE_II = "ENGINE_ION_DRIVE_II"
    ENGINE_HYPER_DRIVE_I = "ENGINE_HYPER_DRIVE_I"


class ShipEngineSchema(BaseModel):
    """Ship Engine Schema."""

    symbol: Annotated[ShipEngineSymbolEnum, Field(description="Symbol of the engine.")]
    name: Annotated[str, Field(description="Name of the engine.")]
    description: Annotated[str, Field(description="Description of the engine.")]
    condition: Annotated[
        float,
        Field(
            description=(
                "The repairable condition of a component."
                "A value of 0 indicates the component needs significant repairs, "
                "while a value of 1 indicates the component is in near perfect condition."
                "As the condition of a component is repaired, the overall integrity of the component decreases."
            ),
            ge=0,
            le=1,
        ),
    ]
    integrity: Annotated[
        float,
        Field(
            description=(
                "The overall integrity of the component, which determines the performance of the component."
                "A value of 0 indicates that the component is almost completely degraded, "
                "while a value of 1 indicates that the component is in near perfect condition."
                "The integrity of the component is non-repairable, and represents permanent wear over time."
            ),
            ge=0,
            le=1,
        ),
    ]
    speed: Annotated[
        int,
        Field(
            description=(
                "The speed stat of this engine."
                "The higher the speed, the faster a ship can travel from one point to another."
                "Reduces the time of arrival when navigating the ship."
            ),
            ge=1,
        ),
    ]
    requirements: Annotated[ShipRequirementSchema, Field(description="The requirements for installation on a ship")]


class ShipModuleSymbolEnum(str, Enum):
    """Ship Module Symbol Enum."""

    MODULE_MINERAL_PROCESSOR_I = "MODULE_MINERAL_PROCESSOR_I"
    MODULE_GAS_PROCESSOR_I = "MODULE_GAS_PROCESSOR_I"
    MODULE_CARGO_HOLD_I = "MODULE_CARGO_HOLD_I"
    MODULE_CARGO_HOLD_II = "MODULE_CARGO_HOLD_II"
    MODULE_CARGO_HOLD_III = "MODULE_CARGO_HOLD_III"
    MODULE_CREW_QUARTERS_I = "MODULE_CREW_QUARTERS_I"
    MODULE_ENVOY_QUARTERS_I = "MODULE_ENVOY_QUARTERS_I"
    MODULE_PASSENGER_CABIN_I = "MODULE_PASSENGER_CABIN_I"
    MODULE_MICRO_REFINERY_I = "MODULE_MICRO_REFINERY_I"
    MODULE_ORE_REFINERY_I = "MODULE_ORE_REFINERY_I"
    MODULE_FUEL_REFINERY_I = "MODULE_FUEL_REFINERY_I"
    MODULE_SCIENCE_LAB_I = "MODULE_SCIENCE_LAB_I"
    MODULE_JUMP_DRIVE_I = "MODULE_JUMP_DRIVE_I"
    MODULE_JUMP_DRIVE_II = "MODULE_JUMP_DRIVE_II"
    MODULE_JUMP_DRIVE_III = "MODULE_JUMP_DRIVE_III"
    MODULE_WARP_DRIVE_I = "MODULE_WARP_DRIVE_I"
    MODULE_WARP_DRIVE_II = "MODULE_WARP_DRIVE_II"
    MODULE_WARP_DRIVE_III = "MODULE_WARP_DRIVE_III"
    MODULE_SHIELD_GENERATOR_I = "MODULE_SHIELD_GENERATOR_I"
    MODULE_SHIELD_GENERATOR_II = "MODULE_SHIELD_GENERATOR_II"


class ShipModuleSchema(BaseModel):
    """Ship Module Schema."""

    symbol: Annotated[ShipModuleSymbolEnum, Field(description="Symbol of the module.")]
    name: Annotated[str, Field(description="Name of the module.")]
    description: Annotated[str, Field(description="Description of the module.")]
    capacityt: Annotated[
        int,
        Field(
            description=(
                "Modules that provide capacity, "
                "such as cargo hold or crew quarters will show this value "
                "to denote how much of a bonus the module grants."
            ),
            ge=0,
            default=0,
        ),
    ] = 0
    range: Annotated[
        int,
        Field(
            description=(
                "Modules that have a range will such as a sensor array show this value "
                "to denote how far can the module reach with its capabilities."
            ),
            ge=0,
            default=0,
        ),
    ] = 0
    requirements: Annotated[ShipRequirementSchema, Field(description="The requirements for installation on a ship")]


class ShipMountSymbolEnum(str, Enum):
    """Ship Mount Symbol Enum."""

    MOUNT_GAS_SIPHON_I = "MOUNT_GAS_SIPHON_I"
    MOUNT_GAS_SIPHON_II = "MOUNT_GAS_SIPHON_II"
    MOUNT_GAS_SIPHON_III = "MOUNT_GAS_SIPHON_III"
    MOUNT_SURVEYOR_I = "MOUNT_SURVEYOR_I"
    MOUNT_SURVEYOR_II = "MOUNT_SURVEYOR_II"
    MOUNT_SURVEYOR_III = "MOUNT_SURVEYOR_III"
    MOUNT_SENSOR_ARRAY_I = "MOUNT_SENSOR_ARRAY_I"
    MOUNT_SENSOR_ARRAY_II = "MOUNT_SENSOR_ARRAY_II"
    MOUNT_SENSOR_ARRAY_III = "MOUNT_SENSOR_ARRAY_III"
    MOUNT_MINING_LASER_I = "MOUNT_MINING_LASER_I"
    MOUNT_MINING_LASER_II = "MOUNT_MINING_LASER_II"
    MOUNT_MINING_LASER_III = "MOUNT_MINING_LASER_III"
    MOUNT_LASER_CANNON_I = "MOUNT_LASER_CANNON_I"
    MOUNT_MISSILE_LAUNCHER_I = "MOUNT_MISSILE_LAUNCHER_I"
    MOUNT_TURRET_I = "MOUNT_TURRET_I"


class ShipMountDepositEnum(str, Enum):
    """Ship Mount Deposit Enum."""

    QUARTZ_SAND = "QUARTZ_SAND"
    SILICON_CRYSTALS = "SILICON_CRYSTALS"
    PRECIOUS_STONES = "PRECIOUS_STONES"
    ICE_WATER = "ICE_WATER"
    AMMONIA_ICE = "AMMONIA_ICE"
    IRON_ORE = "IRON_ORE"
    COPPER_ORE = "COPPER_ORE"
    SILVER_ORE = "SILVER_ORE"
    ALUMINUM_ORE = "ALUMINUM_ORE"
    GOLD_ORE = "GOLD_ORE"
    PLATINUM_ORE = "PLATINUM_ORE"
    DIAMONDS = "DIAMONDS"
    URANITE_ORE = "URANITE_ORE"
    MERITIUM_ORE = "MERITIUM_ORE"


class ShipMountSchema(BaseModel):
    """Ship Mount Schema."""

    symbol: Annotated[ShipMountSymbolEnum, Field(description="Symbol of the mount.")]
    name: Annotated[str, Field(description="Name of the mount.")]
    description: Annotated[str, Field(description="Description of the mount.")]
    strength: Annotated[
        int,
        Field(
            description=(
                "Mounts that have this value, such as mining lasers, denote how powerful this mount's capabilities are."
            ),
            ge=0,
        ),
    ]
    deposits: Annotated[
        List[ShipMountDepositEnum],
        Field(
            description="Mounts that have this value denote what goods can be produced from using the mount.",
            default=[],
        ),
    ] = []
    requirements: Annotated[ShipRequirementSchema, Field(description="The requirements for installation on a ship")]


class ShipCrewRotationEnum(str, Enum):
    """Ship Crew Rotation Enum."""

    STRICT = "STRICT"
    RELAXED = "RELAXED"


class ShipCrewSchema(BaseModel):
    """Ship Crew Schema."""

    current: Annotated[int, Field(description="The current number of crew members on the ship.")]
    required: Annotated[int, Field(description="The minimum number of crew members required to maintain the ship.")]
    capacity: Annotated[int, Field(description="The maximum number of crew members the ship can support.")]
    rotation: Annotated[
        ShipCrewRotationEnum,
        Field(description="The maximum number of crew members the ship can support.", default="STRICT"),
    ] = ShipCrewRotationEnum.STRICT
    morale: Annotated[
        int,
        Field(
            description=(
                "A rough measure of the crew's morale."
                "A higher morale means the crew is happier and more productive."
                "A lower morale means the ship is more prone to accidents."
            ),
            ge=0,
            le=100,
        ),
    ]
    wages: Annotated[
        int,
        Field(
            description=(
                "The amount of credits per crew member paid per hour."
                "Wages are paid when a ship docks at a civilized waypoint."
            ),
            ge=0,
        ),
    ]


class ShipRoleEnum(str, Enum):
    """Ship Role Enum"""

    FABRICATOR = "FABRICATOR"
    HARVESTER = "HARVESTER"
    HAULER = "HAULER"
    INTERCEPTOR = "INTERCEPTOR"
    EXCAVATOR = "EXCAVATOR"
    TRANSPORT = "TRANSPORT"
    REPAIR = "REPAIR"
    SURVEYOR = "SURVEYOR"
    COMMAND = "COMMAND"
    CARRIER = "CARRIER"
    PATROL = "PATROL"
    SATELLITE = "SATELLITE"
    EXPLORER = "EXPLORER"
    REFINERY = "REFINERY"


class ShipRegistrationSchema(BaseModel):
    """Ship Registration Schema."""

    name: Annotated[str, Field(description="The agent's registered name of the ship")]
    factionSymbol: Annotated[str, Field(description="The symbol of the faction the ship is registered with")]
    role: Annotated[ShipRoleEnum, Field(description="The registered role of the ship")]


class ShipNavRouteWaypointSchema(BaseModel):
    """ShipNavRouteWaypointSchema."""

    symbol: Annotated[str, Field(description="The symbol of the waypoint.")]
    type: Annotated[WaypointTypeEnum, Field(description="The type of waypoint.")]
    systemSymbol: Annotated[str, Field(description="The symbol of the system.")]
    x: Annotated[int, Field(description="Position in the universe in the x axis.")]
    y: Annotated[int, Field(description="Position in the universe in the y axis.")]


class ShipNavRouteSchema(BaseModel):
    """Ship Nav Route Schema."""

    destination: Annotated[
        ShipNavRouteWaypointSchema, Field(description="The destination or departure of a ships nav route.")
    ]
    origin: Annotated[
        ShipNavRouteWaypointSchema, Field(description="The destination or departure of a ships nav route.")
    ]
    departureTime: Annotated[str, Field(description="The date time of the ship's departure.")]
    arrival: Annotated[
        str,
        Field(
            description=(
                "The date time of the ship's arrival."
                "If the ship is in-transit, this is the expected time of arrival."
            )
        ),
    ]


class ShipNavStatusEnum(str, Enum):
    """Ship Nav Status Enum."""

    IN_TRANSIT = "IN_TRANSIT"
    IN_ORBIT = "IN_ORBIT"
    DOCKED = "DOCKED"


class ShipNavFlightModeEnum(str, Enum):
    """Ship Nav Flight Mode Enum."""

    DRIFT = "DRIFT"
    STEALTH = "STEALTH"
    CRUISE = "CRUISE"
    BURN = "BURN"


class ShipNavSchema(BaseModel):
    """Ship Nav Schema."""

    systemSymbol: Annotated[str, Field(description="The symbol of the system.")]
    waypointSymbol: Annotated[str, Field(description="The symbol of the waypoint.")]
    route: Annotated[ShipNavRouteSchema, Field(description="")]
    status: Annotated[str, Field(description="The current status of the ship")]
    flightMode: Annotated[
        ShipNavFlightModeEnum,
        Field(
            description="The ship's set speed when traveling between waypoints or systems.",
            default="CRUISE",
        ),
    ] = ShipNavFlightModeEnum.CRUISE


class CooldownSchema(BaseModel):
    """Cooldown Schema."""

    shipSymbol: Annotated[str, Field(description="The symbol of the ship that is on cooldown")]
    totalSeconds: Annotated[int, Field(description="The total duration of the cooldown in seconds", ge=0)]
    remainingSeconds: Annotated[int, Field(description="The remaining duration of the cooldown in seconds", ge=0)]
    expiration: Annotated[
        str, Field(description="The date and time when the cooldown expires in ISO 8601 format", default="")
    ] = ""


class ShipCargoItemSchema(BaseModel):
    """Ship Cargp Item Schema."""

    symbol: Annotated[TradeSymbolEnum, Field(description="The good's symbol.")]
    name: Annotated[str, Field(description="The name of the cargo item type.")]
    description: Annotated[str, Field(description="The description of the cargo item type.")]
    units: Annotated[int, Field(description="The number of units of the cargo item.", ge=1)]


class ShipCargoSchema(BaseModel):
    """Ship Cargp Schema."""

    capacity: Annotated[int, Field(description="The max number of items that can be stored in the cargo hold.", ge=0)]
    units: Annotated[int, Field(description="The number of items currently stored in the cargo hold.", ge=0)] = 0
    inventory: Annotated[List[ShipCargoItemSchema], Field(description="The items currently in the cargo hold.")]


class FuelConsumedSchema(BaseModel):
    """Fuel Consumed Schema."""

    amount: Annotated[int, Field(description="The amount of fuel consumed by the most recent transit or action.", ge=0)]
    timestamp: Annotated[str, Field(description="The time at which the fuel was consumed.")]


class ShipFuelSchema(BaseModel):
    """Ship Fuel Schema."""

    current: Annotated[int, Field(description="The current amount of fuel in the ship's tanks.", ge=0)]
    capacity: Annotated[int, Field(description="The maximum amount of fuel the ship's tanks can hold.", ge=0)]
    consumed: Annotated[
        FuelConsumedSchema,
        Field(
            description=(
                "An object that only shows up when an action has consumed fuel in the process."
                "Shows the fuel consumption data."
            )
        ),
    ]


class ShipSchema(BaseModel):
    """Ship Schema."""

    symbol: Annotated[str, Field(description="Type of ship")]
    registration: Annotated[
        ShipRegistrationSchema,
        Field(description="The public registration information of the ship"),
    ]
    nav: Annotated[
        ShipNavSchema,
        Field(description="The navigation information of the ship."),
    ]
    crew: Annotated[
        ShipCrewSchema,
        Field(description="The ship's crew service and maintain the ship's systems and equipment."),
    ]
    frame: Annotated[
        ShipFrameSchema,
        Field(
            description=(
                "The frame of the ship."
                "The frame determines the number of modules and mounting points of the ship, "
                "as well as base fuel capacity."
                "As the condition of the frame takes more wear, "
                "the ship will become more sluggish and less maneuverable."
            )
        ),
    ]
    reactor: Annotated[
        ShipReactorSchema,
        Field(
            description=(
                "The reactor of the ship. The reactor is responsible for powering the ship's systems and weapons."
            )
        ),
    ]
    engine: Annotated[
        ShipEngineSchema,
        Field(description="The engine determines how quickly a ship travels between waypoints."),
    ]
    cooldown: Annotated[
        CooldownSchema,
        Field(description="A cooldown is a period of time in which a ship cannot perform certain actions."),
    ]
    modules: Annotated[
        List[ShipModuleSchema],
        Field(
            description=(
                "A module can be installed in a ship and provides a set of capabilities such as storage space or "
                "quarters for crew. Module installations are permanent."
            )
        ),
    ]
    mounts: Annotated[
        List[ShipMountSchema],
        Field(description="A mount is installed on the exterier of a ship."),
    ]
    cargo: Annotated[
        ShipCargoSchema,
        Field(description="Ship cargo details."),
    ]
    fuel: Annotated[
        ShipFuelSchema,
        Field(
            description=(
                "Details of the ship's fuel tanks including how much fuel was consumed"
                "during the last transit or action."
            )
        ),
    ]


class ShipResponseSchema(BaseModel):
    """Ship Response Schema."""

    data: ShipSchema


class ListShipsResponseSchema(BaseModel):
    """List Ships Response Schema."""

    data: List[ShipSchema]
    meta: MetaSchema


# ---------------------------------------------------------
# SHIPYARD
# ---------------------------------------------------------
class ShipyardTransactionSchema(BaseModel):
    """Shipyard Transaction Schema."""

    waypointSymbol: Annotated[str, Field(description="The symbol of the waypoint.")]
    shipSymbol: Annotated[str, Field(description="The symbol of the ship that was the subject of the transaction.")]
    shipType: Annotated[str, Field(description="The symbol of the ship that was the subject of the transaction.")]
    price: Annotated[int, Field(description="The price of the transaction.", ge=0)]
    agentSymbol: Annotated[str, Field(description="The symbol of the agent that made the transaction.")]
    timestamp: Annotated[str, Field(description="The timestamp of the transaction.")]


class ShipyardShipCrewSchema(BaseModel):
    """Shipyard Ship Crew Schema."""

    required: Annotated[int, Field(description="Crew required.")]
    capacity: Annotated[int, Field(description="Crew capacity.")]


class ShipyardShipSchema(BaseModel):
    """Shipyard Ship Schema."""

    type: Annotated[ShipTypeEnum, Field(description="Type of ship.")]
    name: Annotated[str, Field(description="Name of ship.")]
    description: Annotated[str, Field(description="Description of ship.")]
    supply: Annotated[str, Field(description="The supply level of a trade good.")]
    activity: Annotated[
        str,
        Field(
            description=(
                "The activity level of a trade good. "
                "If the good is an import, this represents how strong consumption is."
                "If the good is an export, this represents how strong the production is for the good."
                "When activity is strong, consumption or production is near maximum capacity."
                "When activity is weak, consumption or production is near minimum capacity."
            )
        ),
    ]
    purchasePrice: Annotated[int, Field(description="Purchase price of ship")]
    frame: Annotated[
        ShipFrameSchema,
        Field(
            description=(
                "The frame of the ship."
                "The frame determines the number of modules and mounting points of the ship, "
                "as well as base fuel capacity."
                "As the condition of the frame takes more wear, "
                "the ship will become more sluggish and less maneuverable."
            )
        ),
    ]
    reactor: Annotated[
        ShipReactorSchema,
        Field(
            description=(
                "The reactor of the ship. The reactor is responsible for powering the ship's systems and weapons."
            )
        ),
    ]
    engine: Annotated[
        ShipEngineSchema,
        Field(description="The engine determines how quickly a ship travels between waypoints."),
    ]
    modules: Annotated[
        List[ShipModuleSchema],
        Field(
            description=(
                "A module can be installed in a ship and provides a set of capabilities such as storage space or "
                "quarters for crew. Module installations are permanent."
            )
        ),
    ]
    mounts: Annotated[
        List[ShipMountSchema],
        Field(description="A mount is installed on the exterier of a ship."),
    ]
    crew: Annotated[ShipCrewSchema, Field(description="Crew of the ship.")]


class ShipyardSchema(BaseModel):
    """Shipyard Schema."""

    symbol: Annotated[
        str,
        Field(
            description=(
                "The symbol of the shipyard. The symbol is the same as the waypoint where the shipyard is located."
            )
        ),
    ]
    shipTypes: Annotated[
        List[ShipTypeSchema], Field(description="The list of ship types available for purchase at this shipyard.")
    ]
    transactions: Annotated[
        List[ShipyardTransactionSchema], Field(description="The list of recent transactions at this shipyard.")
    ] = []
    ships: Annotated[
        List[ShipyardShipSchema],
        Field(description="The ships that are currently available for purchase at the shipyard."),
    ] = []
    modificationsFee: Annotated[
        int,
        Field(
            description=(
                "The fee to modify a ship at this shipyard."
                "This includes installing or removing modules and mounts on a ship."
                "In the case of mounts, the fee is a flat rate per mount."
                "In the case of modules, the fee is per slot the module occupies."
            )
        ),
    ]


class ShipyardResponseSchema(BaseModel):
    """Shipyard Response Schema."""

    data: ShipyardSchema


# ---------------------------------------------------------
# JUMPGATE
# ---------------------------------------------------------
class JumpGateSchema(BaseModel):
    """Jump Gate Schema."""

    symbol: Annotated[str, Field(description="The symbol of the waypoint.")]
    connections: Annotated[List[str], Field(description="All the gates that are connected to this waypoint.")]


class JumpGateResponseSchema(BaseModel):
    """Jump Gate Response Schema."""

    data: JumpGateSchema


# ---------------------------------------------------------
# CONSTRUCTION
# ---------------------------------------------------------
class ConstructionMaterialSchema(BaseModel):
    """Construction Material Schema."""

    TradeSymbol: Annotated[TradeSymbolEnum, Field(description="The good's symbol.")]
    required: Annotated[int, Field(description="The number of units required.")]
    fullfilled: Annotated[int, Field(description="The number of units fulfilled toward the required amount.")]


class ConstructionSchema(BaseModel):
    """Construction Schema."""

    symbol: Annotated[str, Field(description="The symbol of the waypoint.")]
    materials: Annotated[
        List[ConstructionMaterialSchema], Field(description="The materials required to construct the waypoint.")
    ]
    isComplete: Annotated[bool, Field(description="Whether the waypoint has been constructed.")]


class ConstructionResponseSchema(BaseModel):
    """Construction Response Schema."""

    data: ConstructionSchema


class SupplyConstructionSchema(BaseModel):
    """Supply Construction Schema."""

    construction: Annotated[ConstructionSchema, Field(description="The construction details of a waypoint.")]
    cargo: Annotated[ShipCargoSchema, Field(description="Ship cargo details.")]


class SupplyConstructionResponseSchema(BaseModel):
    """Supply Construction Response Schema."""

    data: SupplyConstructionSchema


# ---------------------------------------------------------
# ACTIONS
# ---------------------------------------------------------
class ShipCargoResponseSchema(BaseModel):
    """Ship Cargo Response Schema."""

    data: ShipCargoSchema


class ShipOrbitNavSchema(BaseModel):
    """Ship Orbit Nav Schema."""

    nav: ShipNavSchema


class ShipOrbitResponseSchema(BaseModel):
    """Ship Orbit Response Schema."""

    data: ShipOrbitNavSchema


class ShipConditionEventEnum(str, Enum):
    """Ship Condition Event Enum."""

    REACTOR_OVERLOAD = "REACTOR_OVERLOAD"
    ENERGY_SPIKE_FROM_MINERAL = "ENERGY_SPIKE_FROM_MINERAL"
    SOLAR_FLARE_INTERFERENCE = "SOLAR_FLARE_INTERFERENCE"
    COOLANT_LEAK = "COOLANT_LEAK"
    POWER_DISTRIBUTION_FLUCTUATION = "POWER_DISTRIBUTION_FLUCTUATION"
    MAGNETIC_FIELD_DISRUPTION = "MAGNETIC_FIELD_DISRUPTION"
    HULL_MICROMETEORITE_STRIKES = "HULL_MICROMETEORITE_STRIKES"
    STRUCTURAL_STRESS_FRACTURES = "STRUCTURAL_STRESS_FRACTURES"
    CORROSIVE_MINERAL_CONTAMINATION = "CORROSIVE_MINERAL_CONTAMINATION"
    THERMAL_EXPANSION_MISMATCH = "THERMAL_EXPANSION_MISMATCH"
    VIBRATION_DAMAGE_FROM_DRILLING = "VIBRATION_DAMAGE_FROM_DRILLING"
    ELECTROMAGNETIC_FIELD_INTERFERENCE = "ELECTROMAGNETIC_FIELD_INTERFERENCE"
    IMPACT_WITH_EXTRACTED_DEBRIS = "IMPACT_WITH_EXTRACTED_DEBRIS"
    FUEL_EFFICIENCY_DEGRADATION = "FUEL_EFFICIENCY_DEGRADATION"
    COOLANT_SYSTEM_AGEING = "COOLANT_SYSTEM_AGEING"
    DUST_MICROABRASIONS = "DUST_MICROABRASIONS"
    THRUSTER_NOZZLE_WEAR = "THRUSTER_NOZZLE_WEAR"
    EXHAUST_PORT_CLOGGING = "EXHAUST_PORT_CLOGGING"
    BEARING_LUBRICATION_FADE = "BEARING_LUBRICATION_FADE"
    SENSOR_CALIBRATION_DRIFT = "SENSOR_CALIBRATION_DRIFT"
    HULL_MICROMETEORITE_DAMAGE = "HULL_MICROMETEORITE_DAMAGE"
    SPACE_DEBRIS_COLLISION = "SPACE_DEBRIS_COLLISION"
    THERMAL_STRESS = "THERMAL_STRESS"
    VIBRATION_OVERLOAD = "VIBRATION_OVERLOAD"
    PRESSURE_DIFFERENTIAL_STRESS = "PRESSURE_DIFFERENTIAL_STRESS"
    ELECTROMAGNETIC_SURGE_EFFECTS = "ELECTROMAGNETIC_SURGE_EFFECTS"
    ATMOSPHERIC_ENTRY_HEAT = "ATMOSPHERIC_ENTRY_HEAT"


class ShipConditionComponentEnum(str, Enum):
    """Ship Condition Component Enum."""

    FRAME = "FRAME"
    REACTOR = "REACTOR"
    ENGINE = "ENGINE"


class ShipConditionEventSchema(BaseModel):
    """Ship Condition Event Schema."""

    symbol: Annotated[str, Field(description="Event symbol")]
    component: Annotated[ShipConditionComponentEnum, Field(description="Event symbol")]
    name: Annotated[str, Field(description="Event symbol")]
    description: Annotated[str, Field(description="Event symbol")]


class NavigateShipSchema(BaseModel):
    """Navigate Ship Response Schema."""

    fuel: ShipFuelSchema
    nav: ShipNavSchema
    events: List[ShipConditionEventSchema]


class NavigateShipResponseSchema(BaseModel):
    """Navigate Ship Response Schema."""

    data: NavigateShipSchema


class RefuelShipSchema(BaseModel):
    """Refuel Ship Response Schema."""

    agent: AgentSchema
    fuel: ShipFuelSchema
    transaction: MarketTranscationSchema


class RefuelShipResponseSchema(BaseModel):
    """Refuel Ship Response Schema."""

    data: RefuelShipSchema


class YieldSchema(BaseModel):
    """Yield Schema."""

    symbol: Annotated[TradeSymbolEnum, Field(description="The good's symbol.")]
    units: Annotated[
        int, Field(description="The number of units extracted that were placed into the ship's cargo hold.")
    ] = 0


class ExtractionSchema(BaseModel):
    """Extraction Response Schema."""

    shipSymbol: Annotated[str, Field(description="Symbol of the ship that executed the extraction.")]
    extracted_resource: Annotated[
        YieldSchema,
        Field(description="A yield from the extraction operation.", alias="yield"),
    ]


class ExtractSchema(BaseModel):
    """Extract Response Schema."""

    cooldown: CooldownSchema
    extraction: ExtractionSchema
    cargo: ShipCargoSchema
    events: List[ShipConditionEventSchema]


class ExtractResponseSchema(BaseModel):
    """Extract Response Schema."""

    data: ExtractSchema


class SurveySizeEnum(str, Enum):
    """Survey Size Enum."""

    SMALL = "SMALL"
    MODERATE = "MODERATE"
    LARGE = "LARGE"


class SurveyDepositSchema(BaseModel):
    """Survey Depost Response Schema."""

    symbol: Annotated[str, Field(description="The symbol of the deposit.")]


class SurveySchema(BaseModel):
    """Survey Response Schema."""

    signature: Annotated[
        str,
        Field(
            description=(
                "A unique signature for the location of this survey."
                "This signature is verified when attempting an extraction using this survey."
            )
        ),
    ]
    symbol: Annotated[str, Field(description="The symbol of the waypoint that this survey is for.")]
    deposits: Annotated[
        List[SurveyDepositSchema],
        Field(
            description=(
                "A list of deposits that can be found at this location."
                "A ship will extract one of these deposits when using this survey in an extraction request."
                "If multiple deposits of the same type are present, the chance of extracting that deposit is increased."
            )
        ),
    ]
    expiration: Annotated[
        str,
        Field(
            description=(
                "The date and time when the survey expires."
                "After this date and time, the survey will no longer be available for extraction."
            )
        ),
    ]
    size: Annotated[
        SurveySizeEnum,
        Field(
            description=(
                "The size of the deposit."
                "This value indicates how much can be extracted from the survey before it is exhausted."
            )
        ),
    ]


class CreateSurveySchema(BaseModel):
    """Create Survey Response Schema."""

    cooldown: CooldownSchema
    surveys: List[SurveySchema]


class CreateSurveyResponseSchema(BaseModel):
    """Create Survey Response Schema."""

    data: CreateSurveySchema
