import React, { Component } from "react";
import { Link } from "react-router-dom";

import { Button, Grid, Typography, TextField, FormControl, FormHelperText, FormControlLabel, Radio, RadioGroup } from "@material-ui/core";
// import Button from "@material-ui/core/Button";
// import Grid from "@material-ui/core/Grid";
// import Typography from "@material-ui/core/Typography";
// import TextField from "@material-ui/core/TextField";
// import FormHelperText from "@material-ui/core/FormHelperText";
// import FormControl from "@material-ui/core/FormControl";
// import Radio from "@material-ui/core/Radio";
// import RadioGroup from "@material-ui/core/RadioGroup";
// import FormControlLabel from "@material-ui/core/FormControlLabel";

export default class CreateRoomPage extends Component {
  defaultVotes = 2;

  constructor(props) {
    super(props);
    this.state = {
      guestCanPause: true,
      votesToSkip: this.defaultVotes,
    };
    // class 내부 함수들이 this keyword를 쓰는 경우 함수를 bind해줘야한다.
    // => 와 같은 형식으로 함수를 선언하면, binding 작업이 필요 없다.
    this.handleRoomButtonPressed = this.handleRoomButtonPressed.bind(this);
    this.handleVotesChange = this.handleVotesChange.bind(this);
    this.handleGuestCanPauseChange = this.handleGuestCanPauseChange.bind(this);
  }

  handleVotesChange(e) {
    this.setState({
      votesToSkip: e.target.value,
    });
  }

  handleGuestCanPauseChange(e) {
    this.setState({
      guestCanPause: e.target.value === "true" ? true : false,
    });
  }

  handleRoomButtonPressed() {
    // server에 JSON 양식으로 보낼 정보를 담고 있다.
    // votes_to_skip처럼 server에서 받을 정보를 그대로 잘 적어줘야한다. spelling matched
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        votes_to_skip: this.state.votesToSkip,
        guest_can_pause: this.state.guestCanPause,
      }),
    };
    // requestOptions를 /api/create-room으로 보내고, response를 받으면,
    // then 그 response를 json object으로 바꾸고,
    // then data를 출력해라! 라는 것
    fetch("/api/create-room", requestOptions)
      .then((response) => response.json())
      .then((data) => this.props.history.push("/room/" + data.code));
  }

  render() {
    return (
      // Grid는 material UI에서 item들은 수직/수평으로 나열할 때 쓴다.
      // CSS flexbox를 사용한다고 한다.
      // container은 수직방향으로 item을 쌓는 것을 의미하며, spacing은 item 사이의 간격이다. 1 = 8pixels
      // item과 같이 다른 속성을 부여할 수도 있다. 다른 내용들은 공식 doc을 찾아보자!
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Typography component="h4" variant="h4">
            Create A Room
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <FormControl component="fieldset">
            <FormHelperText>
              <div align="center">Guest Control of Playback State</div>
            </FormHelperText>
            <RadioGroup row defaultValue="true" onChange={this.handleGuestCanPauseChange}>
              <FormControlLabel value="true" control={<Radio color="primary" />} label="Play/Pause" labelPlacement="bottom" />
              <FormControlLabel value="false" control={<Radio color="secondary" />} label="No Control" labelPlacement="bottom" />
            </RadioGroup>
          </FormControl>
        </Grid>
        <Grid item xs={12} align="center">
          <FormControl>
            <TextField
              required={true}
              type="number"
              onChange={this.handleVotesChange}
              defaultValue={this.defaultVotes}
              inputProps={{
                min: 1,
                style: { textAlign: "center" },
              }}
            />
            <FormHelperText>
              <div align="center">Votes Required To Skip Song</div>
            </FormHelperText>
          </FormControl>
        </Grid>
        <Grid item xs={12} align="center">
          <Button color="primary" variant="contained" onClick={this.handleRoomButtonPressed}>
            Create A Room
          </Button>
        </Grid>
        <Grid item xs={12} align="center">
          <Button color="secondary" variant="contained" to="/" component={Link}>
            Back
          </Button>
        </Grid>
      </Grid>
    );
  }
}
