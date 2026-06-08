# 🚕 Islamabad Ride Fare Chat AI Agent

A conversational AI chatbot that helps users find ride fare rates for cars and bikes across Islamabad sectors.

## Features

✅ **Fare Estimation**: Calculate fares between sectors or by distance  
✅ **Vehicle Support**: Cars (taxi/cab) and bikes (motorcycle)  
✅ **Sector Database**: Comprehensive list of Islamabad sectors (F, G, H, I series + more)  
✅ **Error Handling**: Graceful handling of invalid inputs with helpful suggestions  
✅ **Natural Language**: Understands various query formats and conversational style  
✅ **Text-Based Interface**: Simple CLI chat interface  

## Installation

### Requirements
- Python 3.8 or higher
- NLTK library (optional, for advanced NLP features)

### Setup

1. Clone or download this project
2. Navigate to the project directory
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the chatbot:

```bash
python main.py
```

### Example Queries

```
"What's the fare for a car from F-6 to G-8?"
→ Gets fare estimate between two sectors

"How much does a bike cost for 10 km?"
→ Calculates fare by distance

"Show me available sectors"
→ Lists all available Islamabad sectors

"What's the minimum fare for a car?"
→ Shows pricing information

"Help"
→ Shows help and usage guide
```

## Project Structure

```
├── main.py                 # Entry point and chat loop
├── chatbot.py             # Core chatbot logic
├── fare_database.py       # Islamabad fare data and calculations
├── validators.py          # Input validation and parsing
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## How It Works

### Query Processing
1. User enters a message
2. `validators.py` parses the input to extract:
   - Vehicle type (car/bike)
   - Sectors or distance
   - Intent (fare inquiry, sector list, help)
3. `chatbot.py` processes the parsed information
4. `fare_database.py` calculates and returns fare estimates

### Fare Calculation
- **Base Fare**: Starting charge (car: Rs. 200, bike: Rs. 80)
- **Distance Rate**: Per km charge (car: Rs. 25/km, bike: Rs. 12/km)
- **Minimum Fare**: Ensures minimum charge even for short rides

### Error Handling
- Invalid sector names are caught and user is prompted
- Invalid vehicle types are corrected
- Invalid distances are rejected with guidance
- Missing required information triggers helpful prompts

## Available Sectors

### Blue Zone
F-6, F-7, F-8, F-9, F-10, G-6, G-7, Aabpara, Margalla

### Green Zone
G-8, G-9, G-10, G-11, Shalimar

### Red Zone
H-8, H-9, I-8, I-9, I-10, Bahria, Koral, Chakri, Rawal

## Fare Examples

### Car Fares
- F-6 to G-8: ~Rs. 425 (9 km)
- Margalla to F-9: ~Rs. 375 (7 km)
- 5 km ride: Rs. 325

### Bike Fares
- F-6 to G-8: ~Rs. 228 (9 km)
- Margalla to F-9: ~Rs. 182 (7 km)
- 5 km ride: Rs. 150 (minimum)

## Commands

| Command | Action |
|---------|--------|
| `help` | Show help and usage guide |
| `exit` / `quit` | Close the chatbot |
| `Ctrl+C` | Force exit |

## Future Enhancements

- [ ] Add time-based surge pricing
- [ ] Integration with real database
- [ ] Web interface
- [ ] Multi-language support
- [ ] Real-time traffic factor
- [ ] Booking confirmation

## Development

### Adding New Sectors
Edit `fare_database.py` and add to the `SECTORS` dictionary:

```python
"J-1": {"zone": "blue", "avg_distance_from_center": 15}
```

### Modifying Fares
Update `FARE_CONFIG` in `fare_database.py`:

```python
"car": {
    "base_fare": 200,
    "per_km_rate": 25,
    "minimum_fare": 300
}
```

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions, please refer to the help section in the chatbot (type 'help').

---

Made for Islamabad riders 🇵🇰
