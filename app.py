from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import Markup
import math

app = Flask(__name__)
app.secret_key = 'another_very_secret_key_67890' # CHANGE THIS!

# --- PASTE THE FULL REVISED 'questions' LIST HERE ---
# (The one from the previous response, starting with Tute1_1 (MC), ending Tute1_50 (Num))
questions = [
    # === COORDINATES & DIRECTION ===
    {
        "id_name": "Tute1_1",
        "type": "multichoice",
        "question_text": "<p><strong>Q1</strong> If water has u = -1m/s, what direction is the water travelling?</p>",
        "general_feedback": "<p>u > 0 would represent a current flowing to the east, so u < 0 represents a current flowing westward.</p>",
        "options": [
            {"text": "<![CDATA[Eastward]]>", "fraction": "0"},
            {"text": "<![CDATA[Westward]]>", "fraction": "100"},
            {"text": "<![CDATA[Northward]]>", "fraction": "0"},
            {"text": "<![CDATA[Southward]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["Westward"],
        "hint": "<p><span>Remember u is velocity towards the east, v is velocity towards the north, w is velocity downwards. Consider the sign.</span></p>"
    },
    {
        "id_name": "Tute1_2",
        "type": "multichoice",
        "question_text": "<p><strong>Q2</strong> Water near the base of a waterfall is travelling at 100m/s, Which of the following is true?</p>",
        "general_feedback": "<p>w represents a velocity in the downward direction (positive downwards) i.e. like falling water.</p>",
        "options": [
            {"text": "<![CDATA[w=100m/s]]>", "fraction": "100"},
            {"text": "<![CDATA[w=-100m/s]]>", "fraction": "0"},
            {"text": "<![CDATA[v=100m/s]]>", "fraction": "0"},
            {"text": "<![CDATA[v=-100ms]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["w=100m/s"],
        "hint": "<p><span>Remember u is velocity towards the east, v is velocity towards the north, w is velocity downwards (positive).</span></p>"
    },
    {
        "id_name": "Tute1_3",
        "type": "multichoice",
        "question_text": "<p><strong>Q3</strong> If a car is moving with u=30km/hr, v=-30km/h what direction is it travelling?</p>",
        "general_feedback": "<p>u=30km/hr is Eastward, v=-30km/hr is Southward. Combining these gives South-East.</p>",
        "options": [
            {"text": "<![CDATA[North-West]]>", "fraction": "0"},
            {"text": "<![CDATA[South-East]]>", "fraction": "100"},
            {"text": "<![CDATA[North-East]]>", "fraction": "0"},
            {"text": "<![CDATA[South-West]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["South-East"],
        "hint": "<p><span>Remember u is velocity towards the east, v is velocity towards the north. Consider the sign of v.</span></p>"
    },
    {
        "id_name": "Tute1_14",
        "type": "multichoice",
        "question_text": "<p><strong>Q14</strong> If a current has v = 5 m/s, what cardinal direction is the water travelling?</p>",
        "general_feedback": "<p>v represents velocity towards the North. A positive value means it is flowing in that direction.</p>",
        "options": [
            {"text": "<![CDATA[North]]>", "fraction": "100"},
            {"text": "<![CDATA[South]]>", "fraction": "0"},
            {"text": "<![CDATA[East]]>", "fraction": "0"},
            {"text": "<![CDATA[West]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["North"],
        "hint": "<p><span>Remember u is velocity towards the east, v is velocity towards the north, w is velocity downwards.</span></p>"
    },
    {
        "id_name": "Tute1_15",
        "type": "multichoice",
        "question_text": "<p><strong>Q15</strong> If water is experiencing upwelling at a speed of 0.1 m/s, what is the value of w (the vertical velocity component)?</p>",
        "general_feedback": "<p>w represents velocity downwards (positive downwards). Upwelling is an upward movement, so w must be negative. w = -0.1 m/s.</p>",
        "options": [
            {"text": "<![CDATA[0.1 m/s]]>", "fraction": "0"},
            {"text": "<![CDATA[-0.1 m/s]]>", "fraction": "100"},
            {"text": "<![CDATA[0 m/s]]>", "fraction": "0"},
            {"text": "<![CDATA[Cannot be determined]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["-0.1 m/s"],
        "hint": "<p><span>Consider the sign convention for w (downwards positive). Upwelling means the water is moving upwards.</span></p>"
    },
    {
        "id_name": "Tute1_16",
        "type": "multichoice",
        "question_text": "<p><strong>Q16</strong> A river flows directly South. Which velocity component is non-zero and negative?</p>",
        "general_feedback": "<p>Velocity towards the North is represented by v. If the river flows South, v must be negative.</p>",
        "options": [
            {"text": "<![CDATA[u]]>", "fraction": "0"},
            {"text": "<![CDATA[v]]>", "fraction": "100"},
            {"text": "<![CDATA[w]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["v"],
        "hint": "<p><span>Recall the standard directions for u, v, and w. South is the opposite of North.</span></p>"
    },
    {
        "id_name": "Tute1_25",
        "type": "multichoice",
        "question_text": "<p><strong>Q25</strong> The notation 'x' in physical oceanography typically refers to distance in which direction?</p>",
        "general_feedback": "<p>By convention, x is eastward, y is northward, and z is downward.</p>",
        "options": [
            {"text": "Eastward", "fraction": "100"},
            {"text": "Northward", "fraction": "0"},
            {"text": "Downward", "fraction": "0"},
            {"text": "Upward", "fraction": "0"}
        ],
        "correct_answer_text": ["Eastward"],
        "hint": "<p><span>Recall the standard Cartesian coordinate system used in oceanography.</span></p>"
    },
    {
        "id_name": "Tute1_31",
        "type": "multichoice",
        "question_text": "<p><strong>Q31</strong> A weather balloon is rising at 2 m/s. What is its w velocity component?</p>",
        "general_feedback": "<p>The w component is positive downwards. Since the balloon is rising (moving upwards), its w component is negative. w = -2 m/s.</p>",
        "options": [
            {"text": "<![CDATA[2 m/s]]>", "fraction": "0"},
            {"text": "<![CDATA[-2 m/s]]>", "fraction": "100"},
            {"text": "<![CDATA[0 m/s]]>", "fraction": "0"},
            {"text": "<![CDATA[Not enough information]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["-2 m/s"],
        "hint": "<p><span>Consider the sign convention for the vertical velocity component 'w'.</span></p>"
    },
    {
        "id_name": "Tute1_36",
        "type": "multichoice",
        "question_text": "<p><strong>Q36</strong> If a water parcel has u = 0 m/s, v = -2 m/s, and w = 0 m/s, it is moving:</p>",
        "general_feedback": "<p>u=0 means no East-West movement. v=-2 m/s means movement towards the South at 2 m/s. w=0 means no vertical movement.</p>",
        "options": [
            {"text": "<![CDATA[Eastward at 2 m/s]]>", "fraction": "0"},
            {"text": "<![CDATA[Northward at 2 m/s]]>", "fraction": "0"},
            {"text": "<![CDATA[Southward at 2 m/s]]>", "fraction": "100"},
            {"text": "<![CDATA[Downward at 2 m/s]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["Southward at 2 m/s"],
        "hint": "<p><span>Interpret each velocity component (u, v, w) and its sign.</span></p>"
    },
    {
        "id_name": "Tute1_41",
        "type": "multichoice",
        "question_text": "<p><strong>Q41</strong> If w = 2 m/s, the water is:</p>",
        "general_feedback": "<p>The w component is positive downwards. So w = 2 m/s means the water is sinking or moving downwards at 2 m/s.</p>",
        "options": [
            {"text": "<![CDATA[Moving Eastward at 2 m/s]]>", "fraction": "0"},
            {"text": "<![CDATA[Moving Northward at 2 m/s]]>", "fraction": "0"},
            {"text": "<![CDATA[Moving Downward (sinking) at 2 m/s]]>", "fraction": "100"},
            {"text": "<![CDATA[Moving Upward (rising) at 2 m/s]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["Moving Downward (sinking) at 2 m/s"],
        "hint": "<p><span>Recall the direction associated with the 'w' velocity component and its sign convention.</span></p>"
    },
    {
        "id_name": "Tute1_46",
        "type": "multichoice",
        "question_text": "<p><strong>Q46</strong> If u = -5 km/hr and v = 0 km/hr, what direction is a boat travelling?</p>",
        "general_feedback": "<p>u is eastward velocity. A negative u means westward. v=0 means no north-south motion.</p>",
        "options": [
            {"text": "<![CDATA[Eastward]]>", "fraction": "0"},
            {"text": "<![CDATA[Westward]]>", "fraction": "100"},
            {"text": "<![CDATA[Northward]]>", "fraction": "0"},
            {"text": "<![CDATA[Southward]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["Westward"],
        "hint": "<p><span>Consider the signs of the u and v components.</span></p>"
    },
    {
        "id_name": "Tute1_49",
        "type": "multichoice",
        "question_text": "<p><strong>Q49</strong> A current meter records u=1m/s, v=1m/s, w=0m/s. The water is flowing towards the:</p>",
        "general_feedback": "<p>u=1m/s is Eastward. v=1m/s is Northward. Combining these gives a North-Eastward flow. w=0 means no vertical motion.</p>",
        "options": [
            {"text": "<![CDATA[North]]>", "fraction": "0"},
            {"text": "<![CDATA[East]]>", "fraction": "0"},
            {"text": "<![CDATA[North-East]]>", "fraction": "100"},
            {"text": "<![CDATA[South-West]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["North-East"],
        "hint": "<p><span>Combine the directions indicated by the u and v components.</span></p>"
    },
    # === GRADIENTS ===
    {
        "id_name": "Tute1_5a",
        "type": "multichoice",
        "question_text": "<p><strong>Q5a</strong> An estuary is running northwards, the water gets slower towards the mouth as the width of the estuary increases. At any point on the river, which of the following is true regarding the northward velocity component (v)?</p>",
        "general_feedback": "<p>Since the estuary is running northwards, the v (northward) component of velocity must be positive.</p>",
        "options": [
            {"text": "<![CDATA[v>0]]>", "fraction": "100"},
            {"text": "<![CDATA[v<0]]>", "fraction": "0"},
            {"text": "<![CDATA[u>0]]>", "fraction": "0"},
            {"text": "<![CDATA[u<0]]>", "fraction": "0"},
            {"text": "<![CDATA[w>0]]>", "fraction": "0"},
            {"text": "<![CDATA[w<0]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["v>0"],
        "hint": "<p><span>Remember u is velocity towards the east, v is velocity towards the north, w is velocity downwards. The question specifies the main flow direction.</span></p>"
    },
    {
        "id_name": "Tute1_5b",
        "type": "multichoice",
        "question_text": "<p><strong>Q5b</strong> An estuary is running northwards (positive y-direction), and the water gets slower towards the mouth (further north) as the width of the estuary increases. What can we say about how the northward water velocity (v) changes with northward distance (y)?</p>",
        "general_feedback": "<p>The v (northward) velocity is decreasing as y (northward distance) increases. This means the rate of change of v with respect to y is negative. So, $$ \\frac{dv}{dy}<0 $$</p>",
        "options": [
            {"text": "<![CDATA[$$ \\frac{dv}{dy}<0 $$]]>", "fraction": "100"},
            {"text": "<![CDATA[$$ \\frac{du}{dy}>0 $$]]>", "fraction": "0"},
            {"text": "<![CDATA[$$ \\frac{dv}{dx}>0 $$]]>", "fraction": "0"},
            {"text": "<![CDATA[$$ \\frac{dv}{dx}<0 $$]]>", "fraction": "0"},
            {"text": "<![CDATA[$$ \\frac{du}{dx}<0 $$]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["$$ \\frac{dv}{dy}<0 $$"],
        "hint": "<p><span>The question states the water gets *slower* towards the *mouth* (which is further north). 'v' is northward velocity, 'y' is northward distance. How does 'v' change as 'y' increases?</span></p>"
    },
    {
        "id_name": "Tute1_7a",
        "type": "multichoice",
        "question_text": "<p><strong>Q7a</strong> Water in the Gulf Stream (which flows northwards along the coast of eastern USA) is fastest at the surface and gets slower with depth. How would we express this?</p>",
        "general_feedback": "<p>The Gulf Stream flows northwards, so the relevant velocity component is v. Depth (z) is positive downwards. If velocity gets slower with depth, it means as z increases, v decreases. So the rate of change of v with respect to z, dv/dz, is negative.</p>",
        "options": [
            {"text": "<![CDATA[$$ \\frac{dv}{dz}<0 $$]]>", "fraction": "100"},
            {"text": "<![CDATA[$$ \\frac{dv}{dz}>0 $$]]>", "fraction": "0"},
            {"text": "<![CDATA[$$ \\frac{dv}{dy}>0 $$]]>", "fraction": "0"},
            {"text": "<![CDATA[$$ \\frac{dv}{dy}<0 $$]]>", "fraction": "0"},
            {"text": "<![CDATA[$$ \\frac{du}{dz}>0 $$]]>", "fraction": "0"},
            {"text": "<![CDATA[$$ \\frac{du}{dy}<0 $$]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["$$ \\frac{dv}{dz}<0 $$"],
        "hint": "<p><span>'v' is northward velocity. 'z' is depth (positive downwards). If speed decreases as depth increases, what is the sign of the gradient?</span></p>"
    },
    {
        "id_name": "Tute1_7b",
        "type": "multichoice",
        "question_text": "<p><strong>Q7b</strong> Water in the East Australian Current (which flows southwards along the coast of eastern Australia) is fastest at the surface and gets slower with depth. How would we express this?</p>",
        "general_feedback": "<p>The EAC flows southwards, so its v (northward) component is negative. Let's say at the surface v = -V<sub>max</sub>. As depth (z, positive downwards) increases, the speed gets slower, meaning the magnitude of v becomes smaller (e.g., v becomes -V<sub>mid</sub> where |V<sub>mid</sub>| < |V<sub>max</sub>|). So, as z increases, v becomes *less negative* (i.e., it increases algebraically). Therefore, dv/dz > 0.</p>",
        "options": [
            {"text": "<![CDATA[$$ \\frac{dv}{dz}<0 $$]]>", "fraction": "0"},
            {"text": "<![CDATA[$$ \\frac{dv}{dz}>0 $$]]>", "fraction": "100"},
            {"text": "<![CDATA[$$ \\frac{dv}{dy}>0 $$]]>", "fraction": "0"},
            {"text": "<![CDATA[$$ \\frac{dv}{dy}<0 $$]]>", "fraction": "0"},
            {"text": "<![CDATA[$$ \\frac{du}{dz}>0 $$]]>", "fraction": "0"},
            {"text": "<![CDATA[$$ \\frac{du}{dy}<0 $$]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["$$ \\frac{dv}{dz}>0 $$"],
        "hint": "<p>The current flows South, so 'v' is negative. 'z' is depth (positive downwards). If speed (magnitude) decreases as depth increases, what happens to the (negative) value of 'v'? Does it become more negative or less negative?</p>"
    },
    {
        "id_name": "Tute1_17",
        "type": "multichoice",
        "question_text": "<p><strong>Q17</strong> If dT/dz > 0 in the ocean, what does this mean?</p>",
        "general_feedback": "<p>dT/dz > 0 means that temperature (T) increases as depth (z, positive downwards) increases. So, the water gets warmer with depth.</p>",
        "options": [
            {"text": "<![CDATA[Temperature increases with depth.]]>", "fraction": "100"},
            {"text": "<![CDATA[Temperature decreases with depth.]]>", "fraction": "0"},
            {"text": "<![CDATA[Temperature is constant with depth.]]>", "fraction": "0"},
            {"text": "<![CDATA[Temperature increases towards the surface.]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["Temperature increases with depth."],
        "hint": "<p><span>Remember that z is positive downwards. A positive gradient means the quantity (T) increases in the direction of the coordinate (z).</span></p>"
    },
    {
        "id_name": "Tute1_18", 
        "type": "multichoice",
        "question_text": "<p><strong>Q18</strong> If salinity (S) decreases as you move eastward (positive x-direction), is dS/dx positive or negative?</p>",
        "general_feedback": "<p>The x-direction is eastward. If salinity decreases as x increases, the gradient dS/dx is negative.</p>",
        "options": [
            {"text": "<![CDATA[Positive]]>", "fraction": "0"},
            {"text": "<![CDATA[Negative]]>", "fraction": "100"},
            {"text": "<![CDATA[Zero]]>", "fraction": "0"},
            {"text": "<![CDATA[Cannot be determined]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["Negative"],
        "hint": "<p><span>Consider how the quantity (Salinity) changes as the coordinate (x, eastward) increases. If it decreases, the rate of change is negative.</span></p>"
    },
    {
        "id_name": "Tute1_24", 
        "type": "multichoice",
        "question_text": "<p><strong>Q24</strong> If the concentration of a pollutant (C) is uniform throughout a lake, what is the value of dC/dx (the gradient in the x-direction)?</p>",
        "general_feedback": "<p>If the concentration is uniform, it does not change with position (x). Therefore, the gradient dC/dx is zero.</p>",
        "options": [
            {"text": "<![CDATA[Positive]]>", "fraction": "0"},
            {"text": "<![CDATA[Negative]]>", "fraction": "0"},
            {"text": "<![CDATA[Zero]]>", "fraction": "100"},
            {"text": "<![CDATA[It depends on the pollutant]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["Zero"],
        "hint": "<p><span>A gradient represents a rate of change. If something is uniform, how is it changing with position?</span></p>"
    },
     {
        "id_name": "Tute1_27", 
        "type": "multichoice",
        "question_text": "<p><strong>Q27</strong> If dP/dx = -10 Pa/m, in which direction is the pressure increasing?</p>",
        "general_feedback": "<p>dP/dx is negative, meaning pressure P decreases as x (eastward) increases. Therefore, pressure must be increasing in the opposite direction, which is Westward.</p>",
        "options": [
            {"text": "<![CDATA[Eastward]]>", "fraction": "0"},
            {"text": "<![CDATA[Westward]]>", "fraction": "100"},
            {"text": "<![CDATA[Northward]]>", "fraction": "0"},
            {"text": "<![CDATA[Southward]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["Westward"],
        "hint": "<p><span>A negative gradient means the quantity decreases in the positive direction of the coordinate (x is East). So it increases in the negative direction of that coordinate.</span></p>"
    },
    {
        "id_name": "Tute1_28",
        "type": "numerical",
        "question_text": "<p><strong>Q28</strong> The temperature at the sea surface (z=0m) is 25°C. If dT/dz = -0.1 °C/m, what is the temperature at a depth of 10m? (Answer in °C)</p>",
        "general_feedback": "<p>The change in temperature is $$ \\Delta T = \\frac{dT}{dz} \\times \\Delta z $$. So, $$ \\Delta T = -0.1 \\text{ °C/m} \\times 10 \\text{ m} = -1 \\text{ °C} $$. The new temperature is $$ T_{10m} = T_{0m} + \\Delta T = 25 \\text{ °C} - 1 \\text{ °C} = 24 \\text{ °C} $$.</p>",
        "correct_answer_value": [24.0],
        "hint": "<p><span>Use the gradient to find the change in temperature over the change in depth (ΔT = gradient × Δz). Then add this change to the initial temperature. Remember z is positive downwards.</span></p>"
    },
    {
        "id_name": "Tute1_37", 
        "type": "multichoice",
        "question_text": "<p><strong>Q37</strong> The term dS/dy represents the gradient of salinity (S) in which direction?</p>",
        "general_feedback": "<p>The 'dy' in the denominator indicates a change in the y-direction, which is conventionally Northward.</p>",
        "options": [
            {"text": "<![CDATA[Eastward]]>", "fraction": "0"},
            {"text": "<![CDATA[Northward]]>", "fraction": "100"},
            {"text": "<![CDATA[Downward]]>", "fraction": "0"},
            {"text": "<![CDATA[Upward]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["Northward"],
        "hint": "<p><span>What direction does the coordinate 'y' usually represent in this context?</span></p>"
    },
    {
        "id_name": "Tute1_42", 
        "type": "multichoice",
        "question_text": "<p><strong>Q42</strong> If dH/dy is negative, where H is the height of a wave, what does this imply about the wave height as you move Northward?</p>",
        "general_feedback": "<p>y is the Northward direction. A negative dH/dy means that wave height (H) decreases as y (Northward distance) increases. So, wave height decreases as you move Northward.</p>",
        "options": [
            {"text": "<![CDATA[It increases]]>", "fraction": "0"},
            {"text": "<![CDATA[It decreases]]>", "fraction": "100"},
            {"text": "<![CDATA[It stays the same]]>", "fraction": "0"},
            {"text": "<![CDATA[It oscillates]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["It decreases"],
        "hint": "<p><span>A negative gradient means the quantity (H) decreases in the positive direction of the coordinate (y).</span></p>"
    },
    # === FLUXES ===
    {
        "id_name": "Tute1_12",
        "type": "numerical",
        "question_text": "<p><strong>Q12</strong> Sydney Harbour (close to the Harbour Bridge) has a width of 1.2km and a depth of 50m. If water on an outgoing tide is flowing outwards at 1.2m/s, what is the volume of water leaving the harbour each second? (Answer in m<sup>3</sup>/s)</p>",
        "general_feedback": "<p>Cross-sectional Area = width × depth = 1200m × 50m = 60,000 m<sup>2</sup>. Volume Flux = Area × velocity = 60,000 m<sup>2</sup> × 1.2 m/s = 72,000 m<sup>3</sup>/s</p>",
        "correct_answer_value": [72000.0],
        "hint": "<p><span>The volume of water will be the cross-sectional area that the water is passing through times the speed of the water. Remember to convert km to m.</span></p>"
    },
    {
        "id_name": "Tute1_21",
        "type": "numerical",
        "question_text": "<p><strong>Q21</strong> Water flows through a rectangular channel that is 2m wide and 1m deep. If the velocity of the water is 0.5 m/s, what is the volume flux? (Answer in m<sup>3</sup>/s)</p>",
        "general_feedback": "<p>First, calculate the cross-sectional area: Area = width × depth = 2m × 1m = 2 m<sup>2</sup>. Then, Volume Flux = Area × velocity = 2 m<sup>2</sup> × 0.5 m/s = 1 m<sup>3</sup>/s.</p>",
        "correct_answer_value": [1.0],
        "hint": "<p><span>Volume flux is calculated as Cross-sectional Area × Velocity. First find the area.</span></p>"
    },
    {
        "id_name": "Tute1_22",
        "type": "multichoice",
        "question_text": "<p><strong>Q22</strong> If the velocity of water through a pipe of constant area decreases, what happens to the volume flux?</p>",
        "general_feedback": "<p>Volume Flux = Area × velocity. If Area is constant and velocity decreases, then the Volume Flux must also decrease.</p>",
        "options": [
            {"text": "<![CDATA[It increases.]]>", "fraction": "0"},
            {"text": "<![CDATA[It decreases.]]>", "fraction": "100"},
            {"text": "<![CDATA[It stays the same.]]>", "fraction": "0"},
            {"text": "<![CDATA[It becomes zero.]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["It decreases."],
        "hint": "<p><span>Consider the relationship: Volume Flux = Area × velocity.</span></p>"
    },
    {
        "id_name": "Tute1_29",
        "type": "multichoice",
        "question_text": "<p><strong>Q29</strong> A river narrows, but the volume of water flowing per second (volume flux) remains the same. What happens to the average speed of the water?</p>",
        "general_feedback": "<p>Volume Flux = Area × Speed. If the river narrows, the cross-sectional Area decreases. For the Volume Flux to remain constant, the Speed must increase (principle of continuity).</p>",
        "options": [
            {"text": "<![CDATA[It increases.]]>", "fraction": "100"},
            {"text": "<![CDATA[It decreases.]]>", "fraction": "0"},
            {"text": "<![CDATA[It stays the same.]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["It increases."],
        "hint": "<p><span>Think about the relationship: Flux = Area × Speed. If Flux is constant and Area changes, how must Speed change?</span></p>"
    },
     {
        "id_name": "Tute1_34", 
        "type": "numerical",
        "question_text": "<p><strong>Q34</strong> Volume flux through a strait is 1000 m<sup>3</sup>/s. If the cross-sectional area of the strait is 500 m<sup>2</sup>, what is the average velocity of the water? (Answer in m/s)</p>",
        "general_feedback": "<p>Volume Flux (Q) = Area (A) × Velocity (v). So, v = Q / A.  v = 1000 m<sup>3</sup>/s / 500 m<sup>2</sup> = 2 m/s.</p>",
        "correct_answer_value": [2.0],
        "hint": "<p><span>Rearrange the volume flux equation to solve for velocity.</span></p>"
    },
    {
        "id_name": "Tute1_39",
        "type": "multichoice",
        "question_text": "<p><strong>Q39</strong> If a channel's cross-sectional area is 10 m<sup>2</sup> and water flows through it at 3 m/s, the volume flux is:</p>",
        "general_feedback": "<p>Volume Flux = Area × Velocity = 10 m<sup>2</sup> × 3 m/s = 30 m<sup>3</sup>/s.</p>",
        "options": [
            {"text": "3.33 m<sup>3</sup>/s", "fraction": "0"},
            {"text": "13 m<sup>3</sup>/s", "fraction": "0"},
            {"text": "30 m<sup>3</sup>/s", "fraction": "100"},
            {"text": "300 m<sup>3</sup>/s", "fraction": "0"}
        ],
        "correct_answer_text": ["30 m<sup>3</sup>/s"],
        "hint": "<p><span>Multiply the cross-sectional area by the velocity.</span></p>"
    },
     {
        "id_name": "Tute1_44", 
        "type": "multichoice",
        "question_text": "<p><strong>Q44</strong> A different channel has a cross-sectional area of 20 m<sup>2</sup> and water flows through it at 2.5 m/s. What is the volume flux?</p>",
        "general_feedback": "<p>Volume Flux = Area × Velocity = 20 m<sup>2</sup> × 2.5 m/s = 50 m<sup>3</sup>/s.</p>",
        "options": [
            {"text": "8 m<sup>3</sup>/s", "fraction": "0"},
            {"text": "22.5 m<sup>3</sup>/s", "fraction": "0"},
            {"text": "50 m<sup>3</sup>/s", "fraction": "100"},
            {"text": "500 m<sup>3</sup>/s", "fraction": "0"}
        ],
        "correct_answer_text": ["50 m<sup>3</sup>/s"],
        "hint": "<p><span>Multiply the cross-sectional area by the velocity.</span></p>"
    },
    # === PRESSURE ===
    {
        "id_name": "Tute1_10a",
        "type": "numerical",
        "question_text": "<p><strong>Q10a</strong> Assuming that the density of sea water is 1030 kg/m<sup>3</sup> and g = 10 m/s<sup>2</sup>, what is the water pressure at 100m in the ocean? (Answer in N/m<sup>2</sup>)</p>",
        "general_feedback": "<p>Pressure = depth x density x g = 100m x 1030 kg/m<sup>3</sup> x 10 m/s<sup>2</sup> = 1,030,000 N/m<sup>2</sup>.</p>",
        "correct_answer_value": [1030000.0],
        "hint": "<p><span>hint $$ p=h \\rho g $$</span></p>"
    },
    {
        "id_name": "Tute1_10b",
        "type": "numerical",
        "question_text": "<p><strong>Q10b</strong> Atmospheric pressure is about 100,000 N/m<sup>2</sup>. How far down into the ocean (density 1030 kg/m<sup>3</sup>) would I need to go to increase the pressure by this amount? Use g = 10 m/s<sup>2</sup>. (Answer in m, to one decimal place)</p>",
        "general_feedback": "<p>Pressure= depth x density x g. So, depth = Pressure / (density x g) = 100,000 N/m<sup>2</sup> / (1030 kg/m<sup>3</sup> x 10 m/s<sup>2</sup>) = 100,000 / 10300 ≈ 9.7 m.</p>",
        "correct_answer_value": [9.7],
        "hint": "<p><span>hint $$ p=h \\rho g $$, rearrange for h.</span></p>"
    },
    {
        "id_name": "Tute1_19",
        "type": "numerical",
        "question_text": "<p><strong>Q19</strong> The density of freshwater is 1000 kg/m<sup>3</sup>. What is the pressure at a depth of 10m due to the water alone? Use g = 10 m/s<sup>2</sup>. (Answer in N/m<sup>2</sup>)</p>",
        "general_feedback": "<p>Pressure $$ p = \\rho g h $$. So, $$ p = 1000 \\text{ kg/m}^3 \\times 10 \\text{ m/s}^2 \\times 10 \\text{ m} = 100,000 \\text{ N/m}^2 $$.</p>",
        "correct_answer_value": [100000.0],
        "hint": "<p><span>Use the formula $$ p = \\rho g h $$. Ensure all units are consistent.</span></p>"
    },
    {
        "id_name": "Tute1_20",
        "type": "multichoice",
        "question_text": "<p><strong>Q20</strong> If you dive deeper in the ocean, how does the hydrostatic pressure change (assuming density is constant)?</p>",
        "general_feedback": "<p>Pressure $$ p = \\rho g h $$. As depth (h) increases, pressure (p) increases.</p>",
        "options": [
            {"text": "<![CDATA[It increases.]]>", "fraction": "100"},
            {"text": "<![CDATA[It decreases.]]>", "fraction": "0"},
            {"text": "<![CDATA[It stays the same.]]>", "fraction": "0"},
            {"text": "<![CDATA[It depends on the temperature.]]>", "fraction": "0"}
        ],
        "correct_answer_text": ["It increases."],
        "hint": "<p><span>Think about the weight of the water column above you.</span></p>"
    },
    {
        "id_name": "Tute1_33",
        "type": "numerical",
        "question_text": "<p><strong>Q33</strong> A research submarine is at a depth where the pressure is 500,000 N/m<sup>2</sup>. If the density of seawater is 1025 kg/m<sup>3</sup> and g = 10 m/s<sup>2</sup>, approximately what is the depth of the submarine? (Answer in m, to the nearest meter)</p>",
        "general_feedback": "<p>Using $$ p = \\rho g h $$, we rearrange to $$ h = \\frac{p}{\\rho g} $$. So, $$ h = \\frac{500000 \\text{ N/m}^2}{1025 \\text{ kg/m}^3 \\times 10 \\text{ m/s}^2} = \\frac{500000}{10250} \\approx 48.78 \\text{ m} $$. To the nearest meter, this is 49 m.</p>",
        "correct_answer_value": [49.0],
        "hint": "<p><span>Rearrange the hydrostatic pressure formula to solve for depth (h).</span></p>"
    },
    {
        "id_name": "Tute1_38",
        "type": "numerical",
        "question_text": "<p><strong>Q38</strong> A layer of freshwater (density 1000 kg/m<sup>3</sup>) is 5m thick. What is the pressure at the bottom of this layer due to the freshwater alone? Use g = 10 m/s<sup>2</sup>. (Answer in N/m<sup>2</sup>)</p>",
        "general_feedback": "<p>$$ p = \\rho g h = 1000 \\text{ kg/m}^3 \\times 10 \\text{ m/s}^2 \\times 5 \\text{ m} = 50000 \\text{ N/m}^2 $$.</p>",
        "correct_answer_value": [50000.0],
        "hint": "<p><span>Apply the hydrostatic pressure formula: $$ p = \\rho g h $$.</span></p>"
    },
    {
        "id_name": "Tute1_43",
        "type": "numerical",
        "question_text": "<p><strong>Q43</strong> The pressure at the bottom of a tank due to water is 9800 N/m<sup>2</sup>. If g = 10 m/s<sup>2</sup> and the density of water is 1000 kg/m<sup>3</sup>, what is the depth of the water? (Answer in m)</p>",
        "general_feedback": "<p>Using $$ p = \\rho g h $$, we get $$ h = \\frac{p}{\\rho g} $$. So, $$ h = \\frac{9800 \\text{ N/m}^2}{1000 \\text{ kg/m}^3 \\times 10 \\text{ m/s}^2} = \\frac{9800}{10000} = 0.98 \\text{ m} $$.</p>",
        "correct_answer_value": [0.98],
        "hint": "<p><span>Use the hydrostatic pressure formula and rearrange it to solve for h.</span></p>"
    },
     {
        "id_name": "Tute1_48",
        "type": "numerical",
        "question_text": "<p><strong>Q48</strong> The pressure at a depth of 200m in the ocean (density 1020 kg/m<sup>3</sup>, g = 10 m/s<sup>2</sup>) is 2,040,000 N/m<sup>2</sup>. What is the pressure at a depth of 100m (assuming the same density and g)? (Answer in N/m<sup>2</sup>)</p>",
        "general_feedback": "<p>Pressure is directly proportional to depth ($$p = \\rho g h$$). If the depth is halved (from 200m to 100m), and ρ and g are constant, the pressure will also be halved. So, new pressure = 2,040,000 N/m<sup>2</sup> / 2 = 1,020,000 N/m<sup>2</sup>. Alternatively, calculate directly: $$p = 1020 \\text{ kg/m}^3 \\times 10 \\text{ m/s}^2 \\times 100 \\text{m} = 1,020,000 \\text{ N/m}^2$$.</p>",
        "correct_answer_value": [1020000.0],
        "hint": "<p><span>Pressure is proportional to depth. If depth is halved, what happens to pressure? Or, you can calculate it directly using $$ p = \\rho g h $$.</span></p>"
    },
    # === OTHER (Unit conversions, Speed/Distance/Time, Circumference) ===
    {
        "id_name": "Tute1_6_alt",
        "type": "numerical",
        "question_text": "<p><strong>Q_UnitConv_1</strong> The Antarctic Circumpolar Current flows with a speed of 0.5m/s towards the east. How many kilometers would it travel in one day? (Answer in km, to one decimal place)</p>",
        "general_feedback": "<p>0.5 m/s = 0.5 * (3600 seconds/hour * 24 hours/day) m/day = 0.5 * 86400 m/day = 43200 m/day. To convert to km/day, divide by 1000: 43200 / 1000 = 43.2 km/day.</p>",
        "correct_answer_value": [43.2],
        "hint": "<p><span>Convert m/s to m/day first, then m/day to km/day. There are 86400 seconds in a day.</span></p>"
    },
    {
        "id_name": "Tute1_4_reordered",
        "type": "numerical",
        "question_text": "<p><strong>Q_DistTime_1</strong> An oil slick is travelling at v=0.7m/s carried in the Gulf Stream. How far would it travel in 3 days? (Answer in km, to one decimal place)</p>",
        "general_feedback": "<p>Speed in m/day = 0.7 m/s × (60 s/min × 60 min/hr × 24 hr/day) = 0.7 × 86400 m/day = 60480 m/day. Speed in km/day = 60480 / 1000 = 60.48 km/day. Distance in 3 days = 60.48 km/day × 3 days = 181.44 km. Rounded to one decimal place is 181.4 km.</p>",
        "correct_answer_value": [181.4],
        "hint": "<p><span>Remember distance is speed x time. Convert units carefully: m/s to km/day.</span></p>"
    },
    {
        "id_name": "Tute1_8a_reordered",
        "type": "numerical",
        "question_text": "<p><strong>Q_Circum_1</strong> At 70°S if I start moving northwards and keep going, how far would I need to travel to get back to where I started? [the radius of the earth is 6400km] (Answer in km, to the nearest km)</p>",
        "general_feedback": "<p>The circumference of the earth along lines of constant longitude is always the same. Circumference = 2 × π × Radius = 2 × π × 6400km ≈ 40212.38 km. To the nearest km, this is 40212 km.</p>",
        "correct_answer_value": [40212.0],
        "hint": "<p>Remember $$ Circumference = 2 \\times \\pi \\times Radius$$</p>"
    },
    {
        "id_name": "Tute1_8b_reordered",
        "type": "numerical",
        "question_text": "<p><strong>Q_Circum_2</strong> At 70°S if instead I start moving eastwards and keep going, how far would I need to travel to get back to where I started? [the radius of the earth is 6400km] (Answer in km, to the nearest km)</p>",
        "general_feedback": "<p>The circumference of the earth along lines of constant latitude gets smaller towards the poles. Circumference = 2 × π × Radius × cos(latitude) = 2 × π × 6400km × cos(70°) ≈ 40212.38 km × 0.34202 ≈ 13753.25 km. To the nearest km, this is 13753 km.</p>",
        "correct_answer_value": [13753.0],
        "hint": "<p><span>Remember $$ Circumference at a given latitude = 2 \\times \\pi \\times Radius \\times cos(latitude) $$ Ensure your calculator is in degrees mode for cos(70°).</span></p>"
    },
    {
        "id_name": "Tute1_8c_reordered", 
        "type": "numerical",
        "question_text": "<p><strong>Q_Circum_3</strong> A boat is travelling eastwards at 50km/hr at 70°S. The distance to circumnavigate the planet at this latitude is approximately 13753 km. How long will the boat take? (Answer in days, to one decimal place)</p>",
        "general_feedback": "<p>Time = Distance / Speed = 13753 km / 50 km/hr = 275.06 hours. Time in days = 275.06 hours / 24 hours/day ≈ 11.46 days. To one decimal place: 11.5 days.</p>",
        "correct_answer_value": [11.5],
        "hint": "<p><span>Remember speed = distance/time. So, time = distance/speed.</span></p>"
    },
    {
        "id_name": "Tute1_23",
        "type": "numerical",
        "question_text": "<p><strong>Q_UnitConv_2</strong> A ship travels at 20 knots. Knowing that 1 knot is approximately 0.514 m/s, what is the ship's speed in m/s? (Give your answer to one decimal place).</p>",
        "general_feedback": "<p>Speed in m/s = 20 knots × 0.514 m/s/knot = 10.28 m/s. To one decimal place, this is 10.3 m/s.</p>",
        "correct_answer_value": [10.3],
        "hint": "<p><span>Multiply the speed in knots by the conversion factor.</span></p>"
    },
     {
        "id_name": "Tute1_26",
        "type": "numerical",
        "question_text": "<p><strong>Q_Vector_1</strong> A current has u = 3 m/s and v = 4 m/s. What is the magnitude of its horizontal speed? (Answer in m/s)</p>",
        "general_feedback": "<p>The magnitude of the horizontal speed is found using the Pythagorean theorem: $$ \\text{Speed} = \\sqrt{u^2 + v^2} = \\sqrt{3^2 + 4^2} = \\sqrt{9 + 16} = \\sqrt{25} = 5 \\text{ m/s} $$.</p>",
        "correct_answer_value": [5.0],
        "hint": "<p><span>Use the Pythagorean theorem to combine the u and v components of velocity.</span></p>"
    },
    {
        "id_name": "Tute1_30",
        "type": "numerical",
        "question_text": "<p><strong>Q_UnitConv_3</strong> Atmospheric pressure is approximately 100,000 N/m<sup>2</sup>. What is this pressure in kPa (kilopascals)?</p>",
        "general_feedback": "<p>1 Pascal (Pa) = 1 N/m<sup>2</sup>. 1 kilopascal (kPa) = 1000 Pa. Therefore, 100,000 N/m<sup>2</sup> = 100,000 Pa = 100,000 / 1000 kPa = 100 kPa.</p>",
        "correct_answer_value": [100.0],
        "hint": "<p><span>Remember that 1 N/m<sup>2</sup> is equal to 1 Pascal (Pa). 'kilo' means 1000.</span></p>"
    },
    {
        "id_name": "Tute1_35",
        "type": "numerical",
        "question_text": "<p><strong>Q_UnitConv_4</strong> How many meters are there in 2.5 kilometers? (Answer in m)</p>",
        "general_feedback": "<p>1 kilometer = 1000 meters. So, 2.5 kilometers = 2.5 × 1000 meters = 2500 meters.</p>",
        "correct_answer_value": [2500.0],
        "hint": "<p><span>'kilo' means one thousand.</span></p>"
    },
    {
        "id_name": "Tute1_40",
        "type": "numerical",
        "question_text": "<p><strong>Q_DistTime_2</strong> A drifter moves 150 km in 3 days. What is its average speed in km/day?</p>",
        "general_feedback": "<p>Speed = Distance / Time = 150 km / 3 days = 50 km/day.</p>",
        "correct_answer_value": [50.0],
        "hint": "<p><span>Speed is calculated as Distance divided by Time.</span></p>"
    },
    {
        "id_name": "Tute1_45",
        "type": "numerical",
        "question_text": "<p><strong>Q_UnitConv_5</strong> How many seconds are in half a day? (Answer in s)</p>",
        "general_feedback": "<p>Half a day = 12 hours. 1 hour = 60 minutes. 1 minute = 60 seconds. So, 12 hours × 60 min/hr × 60 s/min = 43200 s.</p>",
        "correct_answer_value": [43200.0],
        "hint": "<p><span>There are 24 hours in a day, 60 minutes in an hour, and 60 seconds in a minute.</span></p>"
    },
    {
        "id_name": "Tute1_50",
        "type": "numerical",
        "question_text": "<p><strong>Q_Vector_2</strong> A swimmer crosses a river. The river flows eastward (u = 0.5 m/s). The swimmer swims northward relative to the water (v = 1 m/s). What is the swimmer's speed relative to the ground? (Answer in m/s, to two decimal places)</p>",
        "general_feedback": "<p>The swimmer's velocity components relative to the ground are u = 0.5 m/s and v = 1 m/s. The speed is the magnitude of this velocity vector: $$ \\text{Speed} = \\sqrt{u^2 + v^2} = \\sqrt{(0.5)^2 + (1)^2} = \\sqrt{0.25 + 1} = \\sqrt{1.25} \\approx 1.118 \\text{ m/s} $$. To two decimal places, this is 1.12 m/s.</p>",
        "correct_answer_value": [1.12],
        "hint": "<p><span>The swimmer's velocity relative to the ground has an eastward component (due to the river) and a northward component (due to their swimming). Use Pythagoras to find the magnitude.</span></p>"
    }
]
# Total of 47 questions after removing Tute1_32 and the image-based ones.
# The original XML had 18 entries, 2 were image based. So 16 original text questions.
# 16 + (50-13 from previous version) = 16 + 37 (original was 13, I added to 50, so 37 new).
# Then I removed Tute1_32 from the new ones, so 36 new text questions.
# 16 original text + 36 new text = 52.
# Ah, my 'questions' list above already had 48 questions from last time (Tute1_11a, Tute1_9a removed)
# Removing Tute1_32 from that makes it 47. That should be correct.

# --- Flask App Code Starts Here ---

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.clear() 
        session['current_question_index'] = 0
        session['user_final_answers'] = [{'answer_text': None, 'is_correct': False} for _ in questions]
        session['question_attempt_status'] = [{'attempts_on_current_visit': 0, 'hint_shown_this_visit': False} for _ in questions]
        session.modified = True
        return redirect(url_for('question_page', q_idx=0))
    return render_template('index.html')

@app.route('/quiz') 
def start_quiz():
    session.clear()
    session['current_question_index'] = 0
    session['user_final_answers'] = [{'answer_text': None, 'is_correct': False} for _ in questions]
    session['question_attempt_status'] = [{'attempts_on_current_visit': 0, 'hint_shown_this_visit': False} for _ in questions]
    session.modified = True
    return redirect(url_for('question_page', q_idx=0))

def check_numerical_answer(user_ans_str, correct_values_list):
    try:
        user_ans_float = float(user_ans_str)
        for correct_ans_float in correct_values_list:
            if math.isclose(user_ans_float, correct_ans_float, rel_tol=0.05):
                return True
        return False
    except ValueError:
        return False

def check_multichoice(user_ans_str, options):
    for opt in options:
        if opt['text'] == user_ans_str: 
            return opt['fraction'] == "100"
    return False

@app.route('/question/<int:q_idx>', methods=['GET', 'POST'])
def question_page(q_idx):
    if 'user_final_answers' not in session:
        return redirect(url_for('start_quiz'))

    if q_idx >= len(questions):
        session['quiz_finished'] = True
        return redirect(url_for('results'))
    
    if request.method == 'GET' and session.pop('navigated_via_panel_flag', False): 
        session['question_attempt_status'][q_idx]['attempts_on_current_visit'] = 0
        session['question_attempt_status'][q_idx]['hint_shown_this_visit'] = False
        session.modified = True

    current_q_data = questions[q_idx]
    attempt_status_for_q = session['question_attempt_status'][q_idx]
    user_previous_answer = session['user_final_answers'][q_idx]['answer_text']
    
    feedback_message = None
    show_hint_now = False
    show_correct_tick_js = False

    if request.method == 'POST':
        user_answer_raw = request.form.get('answer', '')
        user_answer_for_checking = user_answer_raw.strip()

        session['user_final_answers'][q_idx]['answer_text'] = user_answer_raw 
        
        attempt_status_for_q['attempts_on_current_visit'] += 1
        is_correct = False

        if current_q_data['type'] == 'multichoice':
            is_correct = check_multichoice(user_answer_raw, current_q_data['options'])
        elif current_q_data['type'] == 'numerical':
            is_correct = check_numerical_answer(user_answer_for_checking, current_q_data['correct_answer_value'])
        
        session['user_final_answers'][q_idx]['is_correct'] = is_correct

        if is_correct:
            show_correct_tick_js = True
            feedback_message = Markup(current_q_data.get('general_feedback') or "<p class='feedback-correct-text'>Correct!</p>")
            attempt_status_for_q['attempts_on_current_visit'] = 0 
            attempt_status_for_q['hint_shown_this_visit'] = False
        else:
            feedback_message = Markup("<p class='feedback-incorrect-text'>Incorrect. Please try again.</p>")
            if not attempt_status_for_q['hint_shown_this_visit']:
                show_hint_now = True
                attempt_status_for_q['hint_shown_this_visit'] = True
        
        session.modified = True

    display_question = {
        **current_q_data,
        'question_text': Markup(current_q_data['question_text']),
        'general_feedback': Markup(current_q_data.get('general_feedback', '')),
        'hint': Markup(current_q_data.get('hint', ''))
    }

    if current_q_data['type'] == 'multichoice':
        processed_options = []
        for opt in current_q_data['options']:
            option_text_for_display = opt['text']
            if option_text_for_display.startswith("<![CDATA[") and option_text_for_display.endswith("]]>"):
                option_text_for_display = option_text_for_display[len("<![CDATA["):-len("]]>")]
            processed_options.append({'text_html': Markup(option_text_for_display), 'value_attr': opt['text']})
        display_question['options'] = processed_options
    
    nav_panel_status = []
    for i in range(len(questions)):
        final_ans_info = session['user_final_answers'][i]
        status_text = 'unattempted'
        if final_ans_info['answer_text'] is not None: 
            if final_ans_info['is_correct']:
                status_text = 'correct'
            else:
                status_text = 'attempted_incorrect'
        nav_panel_status.append({'number': i + 1, 'status': status_text, 'idx': i})

    return render_template('question.html', 
                           question=display_question, 
                           q_idx=q_idx, 
                           total_questions=len(questions),
                           feedback=feedback_message,
                           show_hint=show_hint_now, 
                           hint_text=Markup(current_q_data.get('hint', '')),
                           nav_panel_status=nav_panel_status,
                           show_correct_tick_js=show_correct_tick_js,
                           user_previous_answer=user_previous_answer,
                           is_question_correct_in_session=session['user_final_answers'][q_idx]['is_correct'])

@app.route('/navigate_to_question/<int:target_q_idx>')
def navigate_to_question(target_q_idx):
    if 'user_final_answers' not in session:
        return redirect(url_for('start_quiz'))
    if 0 <= target_q_idx < len(questions):
        session['current_question_index'] = target_q_idx # Update the main index
        session['navigated_via_panel_flag'] = True 
        session.modified = True
        return redirect(url_for('question_page', q_idx=target_q_idx))
    # Fallback to current or first question if target is invalid
    return redirect(url_for('question_page', q_idx=session.get('current_question_index', 0)))

@app.route('/next_question', methods=['GET']) # Ensure it's GET if called by button via JS redirect
def next_question_logic():
    if 'user_final_answers' not in session:
        return redirect(url_for('start_quiz'))

    current_idx = session.get('current_question_index', 0)
    
    # Simple sequential advance
    next_idx = current_idx + 1
    
    if next_idx >= len(questions):
        session['quiz_finished'] = True
        return redirect(url_for('results'))
    
    session['current_question_index'] = next_idx
    # Reset attempt status for the new question visit
    session['question_attempt_status'][next_idx]['attempts_on_current_visit'] = 0
    session['question_attempt_status'][next_idx]['hint_shown_this_visit'] = False
    session.modified = True
    return redirect(url_for('question_page', q_idx=next_idx))

@app.route('/results')
def results():
    if 'user_final_answers' not in session:
        return redirect(url_for('start_quiz'))

    num_correct = sum(1 for ans_info in session['user_final_answers'] if ans_info['is_correct'])
    
    detailed_results = []
    for i, q_data in enumerate(questions):
        user_ans_info = session['user_final_answers'][i]
        
        correct_ans_display = ""
        if q_data['type'] == 'multichoice':
            for opt in q_data.get('options', []):
                if opt.get('fraction') == "100":
                    text_to_display = opt['text']
                    if text_to_display.startswith("<![CDATA[") and text_to_display.endswith("]]>"):
                         text_to_display = text_to_display[len("<![CDATA["):-len("]]>")]
                    correct_ans_display = Markup(text_to_display)
                    break
        elif q_data['type'] == 'numerical':
            correct_ans_display_val = str(q_data['correct_answer_value'][0])
            unit_str = ""
            q_text_lower = q_data['question_text'].lower()
            unit_marker = "(answer in "
            if unit_marker in q_text_lower:
                unit_start_idx = q_text_lower.find(unit_marker) + len(unit_marker)
                unit_end_idx = q_text_lower.find(')', unit_start_idx)
                if unit_end_idx != -1:
                    unit_str = " " + q_data['question_text'][unit_start_idx:unit_end_idx]
            correct_ans_display = Markup(correct_ans_display_val + unit_str)
        
        detailed_results.append({
            'id_name': Markup(q_data['id_name']),
            'question_text': Markup(q_data['question_text']),
            'user_answer': user_ans_info['answer_text'] if user_ans_info['answer_text'] is not None else "Not attempted",
            'correct_answer_display': correct_ans_display,
            'was_correct': user_ans_info['is_correct'],
            'general_feedback': Markup(q_data.get('general_feedback', ''))
        })

    return render_template('results.html', 
                           score=num_correct, 
                           total_questions=len(questions),
                           results=detailed_results)

if __name__ == '__main__':
    app.run(debug=True)