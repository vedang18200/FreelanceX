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
    
    event JobPosted(uint indexed jobId, address indexed client, string description, uint256 budget);
    event JobTaken(uint indexed jobId, address indexed freelancer);
    event JobCompleted(uint indexed jobId);
    
    function postJob(string memory _description) public payable {
        require(msg.value > 0, "Budget must be greater than zero");
        
        jobs[nextJobId] = Job(
            nextJobId, 
            payable(msg.sender), 
            payable(address(0)), 
            _description, 
            msg.value, 
            Status.Open
        );
        
        emit JobPosted(nextJobId, msg.sender, _description, msg.value);
        nextJobId++;
    }
    
    function takeJob(uint _jobId) public {
        Job storage job = jobs[_jobId];
        require(job.client != address(0), "Job does not exist");
        require(job.status == Status.Open, "Job is not available");
        require(job.client != msg.sender, "Client cannot take their own job");
        
        job.freelancer = payable(msg.sender);
        job.status = Status.InProgress;
        
        emit JobTaken(_jobId, msg.sender);
    }
    
    function completeJob(uint _jobId) public {
        Job storage job = jobs[_jobId];
        require(job.client != address(0), "Job does not exist");
        require(msg.sender == job.client, "Only client can confirm completion");
        require(job.status == Status.InProgress, "Job not in progress");
        
        job.status = Status.Completed;
        job.freelancer.transfer(job.budget);
        
        emit JobCompleted(_jobId);
    }
    
    function getJob(uint _jobId) public view returns (
        uint id,
        address client,
        address freelancer,
        string memory description,
        uint256 budget,
        Status status
    ) {
        Job storage job = jobs[_jobId];
        require(job.client != address(0), "Job does not exist");
        
        return (
            job.id,
            job.client,
            job.freelancer,
            job.description,
            job.budget,
            job.status
        );
    }
    
    function getAllJobs() public view returns (Job[] memory) {
        Job[] memory allJobs = new Job[](nextJobId);
        for (uint i = 0; i < nextJobId; i++) {
            allJobs[i] = jobs[i];
        }
        return allJobs;
    }
    
    function getJobCount() public view returns (uint) {
        return nextJobId;
    }
}