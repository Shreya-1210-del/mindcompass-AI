# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import sys

from fastmcp import FastMCP

# Set up the console logging properly using sys.stderr so that standard logging
# does not disrupt the stdio transport protocol used by MCP.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("WellnessContextServer")

mcp = FastMCP("WellnessContextServer")


@mcp.tool()
def get_mindfulness_exercise(category: str) -> str:
    """Returns specific, structured mindfulness steps based on a category.

    Args:
        category: The category of mindfulness exercise. E.g., 'anxiety', 'grounding', 'focus'.

    Returns:
        Structured mindfulness instructions as a string.
    """
    category_lower = category.lower().strip()
    logger.info(f"Retrieving mindfulness exercise for category: {category}")

    if "anxiety" in category_lower:
        return (
            "### Mindfulness Exercise for Anxiety: 4-7-8 Breathing\n"
            "1. Sit comfortably with your back straight.\n"
            "2. Exhale completely through your mouth, making a whoosh sound.\n"
            "3. Close your mouth and inhale quietly through your nose to a mental count of 4.\n"
            "4. Hold your breath for a count of 7.\n"
            "5. Exhale completely through your mouth, making a whoosh sound to a count of 8.\n"
            "6. Repeat the cycle 4 times."
        )
    elif "grounding" in category_lower:
        return (
            "### Mindfulness Exercise for Grounding: 5-4-3-2-1 Technique\n"
            "Identify and list:\n"
            "- **5 things** you can see around you.\n"
            "- **4 things** you can touch/feel (e.g., the chair under you).\n"
            "- **3 things** you can hear in the distance.\n"
            "- **2 things** you can smell.\n"
            "- **1 thing** you can taste.\n"
            "This technique helps anchor your mind to the present moment."
        )
    elif "focus" in category_lower:
        return (
            "### Mindfulness Exercise for Focus: Box Breathing\n"
            "1. Inhale slowly through your nose for 4 seconds.\n"
            "2. Hold your breath at the top for 4 seconds.\n"
            "3. Exhale slowly through your mouth for 4 seconds.\n"
            "4. Hold your lungs empty for 4 seconds.\n"
            "5. Repeat this loop for 2 to 3 minutes to center your attention."
        )
    else:
        return (
            "### General Mindfulness Exercise: Mindful Body Scan\n"
            "1. Close your eyes and focus on your breath for 3 deep cycles.\n"
            "2. Shift attention to your feet, noticing any tension.\n"
            "3. Slowly scan upwards: calves, knees, thighs, stomach, chest, shoulders, neck, head.\n"
            "4. As you identify areas of tension, consciously release them on each exhale."
        )


@mcp.tool()
def get_cbt_prompt() -> str:
    """Returns clinical-grade cognitive behavioral reflection questions.

    Returns:
        A list of CBT reflection questions as a string.
    """
    logger.info("Retrieving CBT reflection questions.")
    return (
        "Here are clinical-grade Cognitive Behavioral Therapy (CBT) reflection questions to guide your check-in:\n"
        "1. **Situation**: What triggered the current emotion or distress?\n"
        "2. **Automatic Thoughts**: What negative automatic thoughts did you experience? What are you telling yourself about this situation?\n"
        "3. **Cognitive Distortion**: Are you engaging in catastrophizing, mind-reading, or all-or-nothing thinking?\n"
        "4. **Alternative Perspective**: What is the objective evidence for and against this thought? What is a more balanced way to view this situation?\n"
        "5. **Outcome**: How do you feel now after examining the evidence? What is a constructive next step?"
    )


if __name__ == "__main__":
    mcp.run()
