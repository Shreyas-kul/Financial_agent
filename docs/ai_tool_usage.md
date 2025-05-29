# AI Tool Usage Documentation

This document details the AI tools and models used in the development of the AI Market Brief Assistant.

## Speech-to-Text (STT)

### OpenAI Whisper
- **Model Version**: base
- **Usage**: Voice input transcription
- **Implementation**: 
  ```python
  model = whisper.load_model("base")
  result = model.transcribe(audio_array)
  ```
- **Performance**: ~95% accuracy on clear speech

## Text-to-Speech (TTS)

### macOS 'say' Command
- **Usage**: Converting AI responses to speech
- **Implementation**:
  ```python
  subprocess.Popen(['say', '-r', str(rate), text])
  ```
- **Customization**: Adjustable speech rate (100-250 words per minute)

## Market Data Analysis

### Yahoo Finance API (yfinance)
- **Usage**: Real-time market data fetching
- **Implementation**:
  ```python
  stock = yf.Ticker(symbol)
  info = stock.info
  ```
- **Data Points**: Market cap, earnings, price history

## Agent Orchestration

### CrewAI
- **Usage**: Multi-agent system management
- **Implementation**:
  ```python
  crew = Crew(
      agents=agents,
      tasks=tasks,
      process=Process.sequential
  )
  ```
- **Agents**:
  1. Market Analyst
  2. Report Writer

## Development Tools

### Code Generation
- Used for initial project structure
- Generated boilerplate for FastAPI endpoints
- Created basic Streamlit UI components

### Debugging Assistance
- Helped identify type conversion issues in audio processing
- Fixed generator object handling in GPT4All integration
- Resolved async/await patterns in FastAPI

## Model Parameters

### OpenAI Whisper (Speech-to-Text)
- Model: `base`
- Language: Auto-detect
- Task: Transcribe
- Performance: ~95% accuracy for clear speech

### CrewAI Agents

#### Market Analyst Agent
- Model: GPT-4
- Temperature: 0.7
- Max Tokens: 1000
- Tools:
  - Portfolio Exposure Analysis
  - Earnings Surprise Detection
  - Market Sentiment Analysis

#### Report Writer Agent
- Model: GPT-4
- Temperature: 0.5
- Max Tokens: 800
- Focus: Clear, concise market briefs

## Code Generation Steps

1. Initial Project Structure
```bash
mkdir -p agents data_ingestion orchestrator streamlit_app docs
touch requirements.txt README.md
```

2. Market Data Agent Implementation
```python
# Example code generation prompt
"""
Create a MarketDataAgent class that:
1. Fetches Asian tech stock data using yfinance
2. Calculates portfolio exposure
3. Detects earnings surprises
4. Analyzes market sentiment
"""
```

3. CrewAI Integration
```python
# Example code generation prompt
"""
Implement FinancialCrew class using CrewAI to:
1. Orchestrate Market Analyst and Report Writer agents
2. Handle sequential task execution
3. Manage agent communication
"""
```

4. Streamlit UI Development
```python
# Example code generation prompt
"""
Create a Streamlit app with:
1. Voice input/output capabilities
2. Multi-timezone display
3. Text and voice interaction modes
4. Error handling and user feedback
"""
```

## Model Fine-tuning

No specific fine-tuning was required. The models are used with their base configurations and prompted effectively.

## Prompt Engineering

### Market Analysis Prompt Template
```
Analyze the following Asian tech stocks:
- TSMC (TSM)
- Samsung (005930.KS)
- Alibaba (BABA)

Focus on:
1. Portfolio exposure and risk
2. Recent earnings surprises
3. Market sentiment indicators

Format the response in clear, concise bullet points.
```

### Report Generation Prompt Template
```
Convert the following market analysis into a natural language brief:
{analysis}

Requirements:
1. Clear and professional tone
2. Highlight key insights
3. Include relevant numbers/percentages
4. Suitable for voice output
```

## Error Handling

1. Speech Recognition
- Fallback to text input if Whisper fails
- Retry mechanism for unclear audio
- User feedback for audio quality issues

2. Market Data
- Cache frequently requested data
- Handle API rate limits
- Provide fallback data sources

3. Agent Communication
- Timeout handling
- Task repetition detection
- Error state recovery

## Performance Optimization

1. Caching Strategy
- Whisper model caching
- Market data caching
- Agent response caching

2. Resource Management
- Concurrent request handling
- Memory usage optimization
- API call batching

3. Response Time Improvement
- Parallel data fetching
- Optimized prompt templates
- Efficient agent communication

## Deployment Considerations

1. Model Serving
- Whisper model loaded at startup
- Efficient memory management
- Resource scaling

2. API Integration
- Rate limit handling
- Error recovery
- Data validation

3. Monitoring
- Response time tracking
- Error rate monitoring
- Resource usage alerts

## Future Improvements

1. Add support for more language models
2. Implement advanced sentiment analysis
3. Expand market coverage
4. Enhance voice interaction capabilities 