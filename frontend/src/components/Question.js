import React, { Component } from 'react';
import '../stylesheets/Question.css';

class Question extends Component {
  constructor() {
    super();
    this.state = {
      visibleAnswer: false,
    };
  }


  flipVisibility() {
    this.setState({ visibleAnswer: !this.state.visibleAnswer });
  }

  render() {
    const { question, answer, category, difficulty } = this.props;
    const { categories } = this.state; 
    console.log('Category:', category);
    console.log('Category value:', categories && categories[category]);
    return (
      <div className='Question-holder'>
        <div className='Question'>{question}</div>
        <div className='Question-status'>
          <img
            className='category'
            alt={category ? category.toLowerCase() : ''}
            src={category ? `${category.toLowerCase()}.svg` : ''}
          />
          <div className='difficulty'>Difficulty: {difficulty}</div>
          <img
            src='delete.png'
            alt='delete'
            className='delete'
            onClick={() => this.props.questionAction('DELETE')}
          />
        </div>
        <div
          className='show-answer button'
          onClick={() => this.flipVisibility()}
        >
          {this.state.visibleAnswer ? 'Hide' : 'Show'} Answer
        </div>
        <div className='answer-holder'>
          <span
            style={{
              visibility: this.state.visibleAnswer ? 'visible' : 'hidden',
            }}
          >
            Answer: {answer}
          </span>
        </div>
      </div>
    );
  }
}

export default Question;
