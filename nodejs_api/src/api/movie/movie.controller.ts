import {IBasicController} from "api/shared/controllers/IBasicController.interface.js";
import {MoviesService} from "./movie.service.js";

export class MovieController implements IBasicController {
  // PROPERTIES
  routeName = 'movies';
  private moviesService: MoviesService;

  // CTOR
  public constructor () {
    this.moviesService = new MoviesService();
  }

  // METHODS
  public async getMoviesByGenre(req: Request, res: Response): Promise<Response> {
    return res.status(200).json('ok - getMoviesByGenre');
  }

  public async getMoviesBySuggestion(req: Request, res: Response): Promise<Response> {
    return res.status(200).json('ok - getMoviesBySuggestion');
  }

  name(): string {
    return MovieController.name;
  }

}
