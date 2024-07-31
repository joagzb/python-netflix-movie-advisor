const {spawn} = require('child_process');

export class MoviesService implements IBasicService {
  // CTOR
  public constructor () {}


function recommendMovies(userId?, genre?) {
  return new Promise((resolve, reject) => {
    const userIdStr = userId !== null ? userId.toString() : 'None';
    const genreStr = genre !== null ? genre : 'None';

    const pythonProcess = spawn('python', ['recommend_movies.py', userIdStr, genreStr]);

    let result = '';
    let error = '';

    pythonProcess.stdout.on('data', (data) => {
      result += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      error += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        console.error('Error:', err);
        reject(new Error(`Python script exited with code ${code}: ${error}`));
      } else {
        console.log('Recommendations:', result);
        resolve(result);
      }
    });
  });
}

// OVERRIDE
name(): string {
  return MoviesService.name;
}
}