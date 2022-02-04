import React, { Component } from "react";
import RoomJoinPage from "./RoomJoinPage";
import CreateRoomPage from "./CreateRoomPage";
import Room from "./Room";
import { Grid, Button, ButtonGroup, Typography } from "@material-ui/core";
import { BrowserRouter as Router, Switch, Route, Link, Redirect } from "react-router-dom";

export default class HomePage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      roomCode: null,
    };
    this.clearRoomCode = this.clearRoomCode.bind(this);
  }

  // lifecycle!
  // componentDidMount. component가 screen에 처음으로 render 되는 것을 말한다.

  // async라는 keyword는 method이 실행되는 동안 다른 작업이 실행되는 것을 허용한다
  // 즉 method의 작업이 전부 처리되고 나머지 코드들이 실행되지 않게 하는 것
  async componentDidMount() {
    fetch("/api/user-in-room")
      .then((response) => response.json())
      .then((data) => {
        this.setState({
          roomCode: data.code,
        });
      });
  }

  renderHomePage() {
    return (
      <Grid container spacing={3}>
        <Grid item xs={12} align="center">
          <Typography variant="h3" component="h3">
            House Party
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <ButtonGroup variant="contained" color="primary">
            <Button color="primary" to="/join" component={Link}>
              Join a Room
            </Button>
            <Button color="secondary" to="/create" component={Link}>
              Create a Room
            </Button>
          </ButtonGroup>
        </Grid>
      </Grid>
    );
  }

  clearRoomCode() {
    this.setState({
      roomCode: null,
    });
  }

  // Route 내부의 render 속성
  // 해당 path로 연결되었을 때 render이 input으로 받은 것들을 보여준다.
  // 예시의 경우 function을 넣어줌으로써 function에서 반환한 것을 render이 보여줄 것

  render() {
    return (
      <Router>
        <Switch>
          <Route
            exact
            path="/"
            render={() => {
              return this.state.roomCode ? <Redirect to={`/room/${this.state.roomCode}`} /> : this.renderHomePage();
            }}
          />
          <Route path="/join" component={RoomJoinPage} />
          <Route path="/create" component={CreateRoomPage} />
          <Route
            path="/room/:roomCode"
            render={(props) => {
              return <Room {...props} leaveRoomCallback={this.clearRoomCode} />;
            }}
          />
        </Switch>
      </Router>
    );
  }
}
