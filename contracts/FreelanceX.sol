// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FreelanceX {
    enum Status { Open, InProgress, Completed }

    struct Job {
        uint id;
        address payable client;
        address payable freelancer;
        string description;
        uint256 budget;
        Status status;
    }

    uint public nextJobId;
    mapping(uint => Job) public jobs;

    function postJob(string memory _description) public payable {
        require(msg.value > 0, "Budget must be greater than zero");
        jobs[nextJobId] = Job(nextJobId, payable(msg.sender), payable(address(0)), _description, msg.value, Status.Open);
        nextJobId++;
    }

    function takeJob(uint _jobId) public {
        Job storage job = jobs[_jobId];
        require(job.status == Status.Open, "Job is not available");
        job.freelancer = payable(msg.sender);
        job.status = Status.InProgress;
    }

    function completeJob(uint _jobId) public {
        Job storage job = jobs[_jobId];
        require(msg.sender == job.client, "Only client can confirm completion");
        require(job.status == Status.InProgress, "Job not in progress");
        job.status = Status.Completed;
        job.freelancer.transfer(job.budget);
    }

    function getJob(uint _jobId) public view returns (Job memory) {
        return jobs[_jobId];
    }
}
