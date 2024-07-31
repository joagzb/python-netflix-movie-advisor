import {FactoryRouteController} from "api/shared/controllers/FactoryRouteController.class.js";
import {MovieController} from "./movie.controller.js";

class MovieRouter extends FactoryRouteController<MovieController> {

  // CTOR
  public constructor () {
    super(new MovieController());
  }

  // OVERRIDE
  protected initRoutes(): void {
    this.router.get(`/genre/:genre`, (req, res) => this.controller.getMoviesByGenre(req, res));
    this.router.get(`/user/:id`, (req, res) => this.controller.getMoviesBySuggestion(req, res));
  }

  protected initMiddlewares(): void {}
}

export default new MovieRouter();